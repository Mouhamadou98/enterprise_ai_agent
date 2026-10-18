from abc import ABC, abstractmethod

from src.llm.schemas import LLMResponse

class LLMService(ABC):
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Génère une réponse à partir d'un prompt.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def generate_with_tools(self, messages: list[dict], tools: list) -> LLMResponse:
        """
        Génère une réponse en permettant au LLM d'utiliser des tools.
        """
        raise NotImplementedError("Subclasses must implement this method.")