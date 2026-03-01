"""Google Gemini provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import google.generativeai as genai

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class GoogleProvider(BaseLLMProvider):
    """Google Gemini provider."""

    PRICING = {
        "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
        "gemini-1.5-flash": {"input": 0.00035, "output": 0.00105},
        "gemini-pro": {"input": 0.0005, "output": 0.0015},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    @property
    def name(self) -> str:
        return "google"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model_name = opts.model or "gemini-1.5-flash"

        model = genai.GenerativeModel(model_name)

        # Convert messages to Gemini format
        contents = []
        for m in messages:
            if m.role == "system":
                # Gemini doesn't have system role, prepend to first user message
                continue
            contents.append(m.content)

        response = await model.generate_content_async(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=opts.temperature,
                max_output_tokens=opts.max_tokens,
                top_p=opts.top_p,
                top_k=opts.top_k,
            ),
        )

        return LLMResponse(
            content=response.text if response.text else "",
            model=model_name,
            usage={
                "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
            },
            finish_reason=response.candidates[0].finish_reason.name if response.candidates else None,
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model_name = opts.model or "gemini-1.5-flash"

        model = genai.GenerativeModel(model_name)

        contents = []
        for m in messages:
            if m.role == "system":
                continue
            contents.append(m.content)

        response = await model.generate_content_async(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=opts.temperature,
                max_output_tokens=opts.max_tokens,
                top_p=opts.top_p,
                top_k=opts.top_k,
            ),
            stream=True,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["gemini-1.5-flash"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
