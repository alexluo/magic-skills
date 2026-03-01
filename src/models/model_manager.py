"""Model manager for handling multiple LLM providers."""

import os
from typing import Dict, List, Optional, Type

from .base_provider import BaseLLMProvider, LLMMessage, LLMOptions, LLMResponse
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .qwen_provider import QwenProvider
from .ernie_provider import ERNIEProvider
from .spark_provider import SparkProvider
from .kimi_provider import KimiProvider
from .deepseek_provider import DeepSeekProvider
from .meta_provider import MetaProvider
from .mistral_provider import MistralProvider
from .cohere_provider import CohereProvider


class ModelManager:
    """Manages multiple LLM providers."""

    PROVIDERS: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "qwen": QwenProvider,
        "ernie": ERNIEProvider,
        "spark": SparkProvider,
        "kimi": KimiProvider,
        "deepseek": DeepSeekProvider,
        "meta": MetaProvider,
        "mistral": MistralProvider,
        "cohere": CohereProvider,
    }

    def __init__(self):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._default_provider = "openai"
        self._default_model = "gpt-4o-mini"

    def register_provider(self, name: str, provider: BaseLLMProvider) -> None:
        """Register a provider instance."""
        self._providers[name] = provider

    def get_provider(self, name: Optional[str] = None) -> BaseLLMProvider:
        """Get a provider by name or default."""
        name = name or self._default_provider
        if name not in self._providers:
            # Auto-initialize if not exists
            if name in self.PROVIDERS:
                self._providers[name] = self.PROVIDERS[name]()
            else:
                raise ValueError(f"Unknown provider: {name}")
        return self._providers[name]

    def set_default_provider(self, name: str, model: Optional[str] = None) -> None:
        """Set default provider and model."""
        self._default_provider = name
        if model:
            self._default_model = model

    async def generate(
        self,
        messages: List[LLMMessage],
        provider: Optional[str] = None,
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        """Generate response using specified or default provider."""
        prov = self.get_provider(provider)
        opts = options or LLMOptions()
        if not opts.model:
            opts.model = self._default_model
        return await prov.generate(messages, opts)

    async def stream(
        self,
        messages: List[LLMMessage],
        provider: Optional[str] = None,
        options: Optional[LLMOptions] = None
    ):
        """Stream response using specified or default provider."""
        prov = self.get_provider(provider)
        opts = options or LLMOptions()
        if not opts.model:
            opts.model = self._default_model
        async for chunk in prov.stream(messages, opts):
            yield chunk

    def list_providers(self) -> List[str]:
        """List available providers."""
        return list(self.PROVIDERS.keys())

    def list_models(self, provider: Optional[str] = None) -> List[str]:
        """List available models for a provider."""
        prov = self.get_provider(provider)
        return prov.supported_models

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        provider: Optional[str] = None,
        model: Optional[str] = None
    ) -> float:
        """Estimate cost for token usage."""
        prov = self.get_provider(provider)
        model = model or self._default_model
        return prov.estimate_cost(input_tokens, output_tokens, model)
