from typing import TypedDict



class AgentState(TypedDict):

    messages: list[dict]
    tool_calls: list[dict]

