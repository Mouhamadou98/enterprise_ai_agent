from src.llm.base import LLMService
from src.config import settings
from src.llm.providers.ollama import OllamaLLM


class LLMFactory:

    @staticmethod
    def create() -> LLMService:

        provider = settings.llm_provider.lower()

        if provider == "openai":
            raise NotImplementedError("OpenAI provider not implemented yet")

        if provider == "mistral":
            raise NotImplementedError("Mistral provider not implemented yet")

        if provider == "gemini":
            raise NotImplementedError("Gemini provider not implemented yet")

        if provider == "ollama":
            return OllamaLLM()
        
        raise ValueError(
            f"LLM provider inconnu : {settings.llm_provider}"
        )