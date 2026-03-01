"""Baidu ERNIE provider implementation."""

import os
from typing import AsyncIterator, List, Optional

import httpx

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse


class ERNIEProvider(BaseLLMProvider):
    """Baidu ERNIE provider."""

    PRICING = {
        "ernie-4.0": {"input": 0.012, "output": 0.012},
        "ernie-3.5": {"input": 0.004, "output": 0.004},
        "ernie-speed": {"input": 0.001, "output": 0.001},
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.api_key = api_key or os.getenv("ERNIE_API_KEY")
        self.secret_key = os.getenv("ERNIE_SECRET_KEY")
        self.base_url = base_url or "https://aip.baidubce.com"

    @property
    def name(self) -> str:
        return "ernie"

    @property
    def supported_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def _get_access_token(self) -> str:
        """Get Baidu access token."""
        url = f"{self.base_url}/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params)
            data = response.json()
            return data.get("access_token", "")

    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        opts = options or LLMOptions()
        model = opts.model or "ernie-3.5"

        access_token = await self._get_access_token()
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}"

        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": opts.temperature,
            "max_output_tokens": opts.max_tokens or 2048,
            "top_p": opts.top_p,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                params={"access_token": access_token},
                json=payload,
            )
            data = response.json()

        return LLMResponse(
            content=data.get("result", ""),
            model=model,
            usage={
                "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
                "total_tokens": data.get("usage", {}).get("total_tokens", 0),
            },
        )

    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        opts = options or LLMOptions()
        model = opts.model or "ernie-3.5"

        access_token = await self._get_access_token()
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}"

        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": opts.temperature,
            "max_output_tokens": opts.max_tokens or 2048,
            "top_p": opts.top_p,
            "stream": True,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url,
                headers=headers,
                params={"access_token": access_token},
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data != "[DONE]":
                            yield data

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        pricing = self.PRICING.get(model, self.PRICING["ernie-3.5"])
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost
