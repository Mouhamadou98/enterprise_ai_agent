import pytest

from src.config import settings
from src.llm.factory import LLMFactory


@pytest.mark.parametrize(
    "provider",
    ["openai", "mistral", "gemini"],
)
def test_supported_providers_are_recognized(monkeypatch, provider):
    monkeypatch.setattr(
        settings,
        "llm_provider",
        provider,
    )

    with pytest.raises(NotImplementedError):
        LLMFactory.create()


def test_unknown_provider():

    original_provider = settings.llm_provider

    settings.llm_provider = "unknown"

    try:
        with pytest.raises(ValueError):
            LLMFactory.create()
    finally:
        settings.llm_provider = original_provider