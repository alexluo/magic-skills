"""Tests for ModelManager."""

import pytest
import os
from unittest.mock import patch, MagicMock

from src.models import ModelManager, LLMMessage


@pytest.fixture
def model_manager():
    """Create ModelManager instance."""
    return ModelManager()


def test_list_providers(model_manager):
    """Test listing providers."""
    providers = model_manager.list_providers()

    assert "openai" in providers
    assert "anthropic" in providers
    assert "google" in providers
    assert len(providers) >= 11  # All 12 providers


def test_set_default_provider(model_manager):
    """Test setting default provider."""
    model_manager.set_default_provider("anthropic", "claude-3-sonnet")

    provider = model_manager.get_provider()
    assert provider is not None


@pytest.mark.asyncio
async def test_generate_without_api_key(model_manager):
    """Test generate without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(Exception):
            await model_manager.generate(
                messages=[LLMMessage(role="user", content="Hello")]
            )


def test_estimate_cost(model_manager):
    """Test cost estimation."""
    # Mock the provider to avoid needing API key
    mock_provider = MagicMock()
    mock_provider.estimate_cost.return_value = 0.0018
    
    model_manager._providers["openai"] = mock_provider
    
    cost = model_manager.estimate_cost(
        input_tokens=1000,
        output_tokens=500,
        provider="openai",
        model="gpt-4o-mini"
    )

    assert cost > 0
    assert cost == 0.0018


def test_get_provider_auto_init(model_manager):
    """Test provider auto-initialization."""
    # Should auto-initialize when not in cache
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        provider = model_manager.get_provider("openai")
        assert provider is not None
