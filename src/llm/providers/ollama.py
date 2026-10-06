from ollama import Client

from src.config import settings
from src.llm.base import LLMService


class OllamaLLM(LLMService):

    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or settings.ollama_model
        self.client = Client(host=base_url or settings.ollama_base_url)

    def generate_text(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    
    def generate_with_tools(self, messages, tools) -> object:

        ollama_tools = []

        for tool in tools:
            ollama_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.args_schema.model_json_schema(),
                    },
                }
            )

        response = self.client.chat(
            model=self.model,
            messages=messages,
            tools=ollama_tools,
        )
        
        return response