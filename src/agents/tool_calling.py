from src.llm.base import LLMService
from src.agents.tool_executor import ToolExecutor


class ToolCallingAgent:

    def __init__(self, llm: LLMService, tools: ToolExecutor):
        self.llm = llm
        self.tools = tools
        self.executor = ToolExecutor(tools)

    def run(self, message: str) -> str:

        messages = [
            {
                "role": "user",
                "content": message,
            }
        ]

        # 1. Demander au LLM s'il doit utiliser un tool
        response = self.llm.generate_with_tools(
            messages=messages,
            tools=self.tools,
        )

        # 2. Si aucun tool n'est demandé,
        # retourner directement la réponse
        if not response.message.tool_calls:
            return response.message.content

        # 3. Pour l'instant, on traite le premier tool call
        tool_call = response.message.tool_calls[0]

        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        # 4. Exécuter le tool
        result = self.executor.execute(
            tool_name=tool_name,
            arguments=arguments,
        )

        # 5. Ajouter la réponse du LLM à l'historique
        messages.append({
            "role": "assistant",
            "content": response.message.content or "",
            "tool_calls": response.message.tool_calls,
        })

        # 6. Ajouter le résultat du tool
        messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": str(result),
        })

        # 7. Demander au LLM de produire la réponse finale
        final_response = self.llm.generate_with_tools(
            messages=messages,
            tools=self.tools,
        )

        return final_response.message.content