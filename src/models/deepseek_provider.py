"""DeepSeek provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import httpx

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek provider."""

    PRICING = {
        "deepseek-chat": {"input": 0.0015, "output": 0.003},
        "deepseek-coder": {"input": 0.0015, "output": 0.003},
        "deepseek-reasoner": {"input": 0.003, "output": 0.006},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or "https://api.deepseek.com"

    @property
    def name(self) -> str:
        return "deepseek"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model = opts.model or "deepseek-chat"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": opts.temperature,
            "max_tokens": opts.max_tokens or 2048,
            "top_p": opts.top_p,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            data = response.json()

        choice = data.get("choices", [{}])[0]
        usage = data.get("usage", {})

        return LLMResponse(
            content=choice.get("message", {}).get("content", ""),
            model=model,
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            finish_reason=choice.get("finish_reason"),
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model = opts.model or "deepseek-chat"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": opts.temperature,
            "max_tokens": opts.max_tokens or 2048,
            "top_p": opts.top_p,
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            yield data

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["deepseek-chat"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
