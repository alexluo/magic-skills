"""Alibaba Qwen provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import httpx

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class QwenProvider(BaseLLMProvider):
    """Alibaba Qwen provider."""

    PRICING = {
        "qwen-max": {"input": 0.002, "output": 0.006},
        "qwen-plus": {"input": 0.001, "output": 0.003},
        "qwen-turbo": {"input": 0.0005, "output": 0.0015},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.base_url = base_url or "https://dashscope.aliyuncs.com/api/v1"

    @property
    def name(self) -> str:
        return "qwen"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model = opts.model or "qwen-turbo"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "input": {
                "messages": [{"role": m.role, "content": m.content} for m in messages]
            },
            "parameters": {
                "temperature": opts.temperature,
                "max_tokens": opts.max_tokens or 2048,
                "top_p": opts.top_p,
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        output = data.get("output", {})
        usage = data.get("usage", {})

        return LLMResponse(
            content=output.get("text", ""),
            model=model,
            usage={
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            finish_reason=output.get("finish_reason"),
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model = opts.model or "qwen-turbo"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "input": {
                "messages": [{"role": m.role, "content": m.content} for m in messages]
            },
            "parameters": {
                "temperature": opts.temperature,
                "max_tokens": opts.max_tokens or 2048,
                "top_p": opts.top_p,
            },
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=headers,
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            yield data

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["qwen-turbo"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
