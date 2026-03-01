"""Anthropic Claude provider implementation."""

import os
from typing import AsyncIterator, List, Optional

from anthropic import AsyncAnthropic

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""

    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
        "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
        "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self._client = AsyncAnthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            base_url=base_url
        )

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model = opts.model or "claude-3-5-sonnet-20241022"

        # Separate system message
        system_msg = ""
        user_messages = []
        for m in messages:
            if m.role == "system":
                system_msg = m.content
            else:
                user_messages.append({"role": m.role, "content": m.content})

        response = await self._client.messages.create(
            model=model,
            max_tokens=opts.max_tokens or 4096,
            temperature=opts.temperature,
            top_p=opts.top_p,
            system=system_msg if system_msg else None,
            messages=user_messages,
        )

        return LLMResponse(
            content=response.content[0].text if response.content else "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            finish_reason=response.stop_reason,
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model = opts.model or "claude-3-5-sonnet-20241022"

        system_msg = ""
        user_messages = []
        for m in messages:
            if m.role == "system":
                system_msg = m.content
            else:
                user_messages.append({"role": m.role, "content": m.content})

        async with self._client.messages.stream(
            model=model,
            max_tokens=opts.max_tokens or 4096,
            temperature=opts.temperature,
            top_p=opts.top_p,
            system=system_msg if system_msg else None,
            messages=user_messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["claude-3-5-sonnet-20241022"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
