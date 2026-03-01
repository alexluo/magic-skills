"""Cohere provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import httpx

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class CohereProvider(BaseLLMProvider):
    """Cohere provider."""

    PRICING = {
        "command-r-plus": {"input": 0.003, "output": 0.015},
        "command-r": {"input": 0.0015, "output": 0.0075},
        "command": {"input": 0.001, "output": 0.002},
        "command-light": {"input": 0.0005, "output": 0.001},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        self.base_url = base_url or "https://api.cohere.ai"

    @property
    def name(self) -> str:
        return "cohere"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model = opts.model or "command-r"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Convert messages to Cohere format
        chat_history = []
        message = ""
        for i, m in enumerate(messages):
            if i == len(messages) - 1 and m.role == "user":
                message = m.content
            else:
                chat_history.append({"role": m.role, "message": m.content})

        payload = {
            "model": model,
            "message": message,
            "chat_history": chat_history,
            "temperature": opts.temperature,
            "max_tokens": opts.max_tokens or 2048,
            "p": opts.top_p,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat",
                headers=headers,
                json=payload,
            )
            data = response.json()

        return LLMResponse(
            content=data.get("text", ""),
            model=model,
            usage={
                "prompt_tokens": data.get("meta", {}).get("tokens", {}).get("input_tokens", 0),
                "completion_tokens": data.get("meta", {}).get("tokens", {}).get("output_tokens", 0),
                "total_tokens": data.get("meta", {}).get("tokens", {}).get("total_tokens", 0),
            },
            finish_reason=data.get("finish_reason"),
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model = opts.model or "command-r"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        chat_history = []
        message = ""
        for i, m in enumerate(messages):
            if i == len(messages) - 1 and m.role == "user":
                message = m.content
            else:
                chat_history.append({"role": m.role, "message": m.content})

        payload = {
            "model": model,
            "message": message,
            "chat_history": chat_history,
            "temperature": opts.temperature,
            "max_tokens": opts.max_tokens or 2048,
            "p": opts.top_p,
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/v1/chat",
                headers=headers,
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        yield line

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["command-r"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
