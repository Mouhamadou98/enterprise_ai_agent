from ollama import Client

from src.config import settings
from src.llm.base import LLMService
from src.llm.schemas import LLMResponse, ToolCall


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
    
    def generate_with_tools(self, messages: list[dict], tools: list) -> LLMResponse:

        ollama_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.args_schema.model_json_schema()
                }
            }
            for tool in tools
        ]

        response = self.client.chat(   
            model=self.model,
            messages=messages,
            tools=ollama_tools,
            options={
                "temperature": 0.1,
            },
        )

        messages = response.message
        tool_calls = [
            ToolCall(
                tool_name=call.function.name,
                arguments=call.function.arguments
            )
            for call in (messages.tool_calls or [])
        ]

        response = LLMResponse(
            content=messages.content or "",
            tool_calls=tool_calls,
        )
        return response