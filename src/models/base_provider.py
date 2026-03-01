"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional

from pydantic import BaseModel


class LLMMessage(BaseModel):
    """LLM message model."""

    role: str  # "system", "user", "assistant"
    content: str


class LLMOptions(BaseModel):
    """LLM generation options."""

    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: Optional[int] = None
    stop: Optional[List[str]] = None
    model: Optional[str] = None


class LLMResponse(BaseModel):
    """LLM response model."""

    content: str
    model: str
    usage: Dict[str, int] = {}
    finish_reason: Optional[str] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url
        self._client = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass

    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """List of supported models."""
        pass

    @abstractmethod
    async def generate(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> LLMResponse:
        """Generate response from messages."""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[LLMMessage],
        options: Optional[LLMOptions] = None
    ) -> AsyncIterator[str]:
        """Stream response from messages."""
        pass

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """Count tokens in text."""
        # Simple approximation: 1 token ≈ 4 characters
        return len(text) // 4

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Estimate cost for token usage."""
        # Override in specific providers
        return 0.0
