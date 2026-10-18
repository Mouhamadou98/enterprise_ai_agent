
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ToolExecutionError(Exception):
    """Erreur survenue pendant l'exécution d'un outil métier."""


class ToolExecutor:

    def __init__(self, tools: list):
        self.tools = {
            tool.name: tool
            for tool in tools
        }

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        tool = self.tools.get(tool_name)

        if tool is None:
            raise ToolExecutionError(
                f"Unknown tool: {tool_name}"
            )

        try:
            return tool.invoke(arguments)

        except Exception as exc:
            logger.exception(
                "Tool execution failed: %s",
                tool_name,
            )
            raise ToolExecutionError(
                f"Tool '{tool_name}' failed."
            ) from exc
