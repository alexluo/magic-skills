"""OpenAI LLM provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import tiktoken
from openai import AsyncOpenAI

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""

    # Pricing per 1K tokens (as of 2024)
    PRICING = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self._client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url
        )

    @property
    def name(self) -> str:
        return "openai"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        """Generate response using OpenAI API."""
        opts = options or LLMOptions()
        model = opts.model or "gpt-4o-mini"

        response = await self._client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=opts.temperature,
            max_tokens=opts.max_tokens,
            top_p=opts.top_p,
            stop=opts.stop,
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            finish_reason=response.choices[0].finish_reason,
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        """Stream response using OpenAI API."""
        opts = options or LLMOptions()
        model = opts.model or "gpt-4o-mini"

        stream = await self._client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=opts.temperature,
            max_tokens=opts.max_tokens,
            top_p=opts.top_p,
            stop=opts.stop,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """Count tokens using tiktoken."""
        model = model or "gpt-4o-mini"
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            return super().count_tokens(text, model)

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Estimate cost for OpenAI API usage."""
        pricing = self.PRICING.get(model, self.PRICING["gpt-4o-mini"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
