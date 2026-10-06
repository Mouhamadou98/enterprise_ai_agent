from src.llm.base import LLMService


class FakeLLMService(LLMService):

    def generate_text(self, prompt: str) -> str:
        return f"Réponse générée pour : {prompt}"
    
    def generate_with_tools(self, messages, tools):
        return None