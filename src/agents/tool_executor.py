class ToolExecutor:

    def __init__(self, tools: list):
        self.tools = {
            tool.name: tool
            for tool in tools
        }

    def execute(self, tool_name: str, arguments: dict):
        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        return tool.invoke(arguments)