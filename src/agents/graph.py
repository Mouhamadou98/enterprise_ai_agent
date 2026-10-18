from typing import Any

from langgraph.graph import END, START ,StateGraph

from src.llm.prompts import PromptBuilder

from src.agents.state import AgentState
from src.agents.tool_executor import ToolExecutor
from src.llm.base import LLMService

def build_agent_graph(llm: LLMService, tools: list) :
    
    executor = ToolExecutor(tools)

    def agent_node(state: AgentState) -> dict[str,Any]:
        messages = list(state["messages"])

        if not any(message.get("role") == "system" for message in messages):
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": PromptBuilder.build_agent_system_prompt(),
                },
            )

        response = llm.generate_with_tools(
            messages=messages,
            tools=tools,
        )
        # print("LLM CONTENT:", response.content)
        # print("LLM TOOL CALLS:", response.tool_calls) 

        assistant_message = {
            "role": "assistant",
            "content": response.content or "",
            "tool_calls": [
                {
                    "function": {
                        "name": call.tool_name,
                        "arguments": call.arguments
                    }
                }
                for call in response.tool_calls
            ],
        }

        return {
            "messages": messages + [assistant_message],
            "tool_calls": [
                {
                    "name": call.tool_name,
                    "arguments": call.arguments,
                }
                for call in response.tool_calls
            ],
        }
      
    def tools_node(state: AgentState) -> dict[str, Any]:
        # print("TOOLS TO EXECUTE:", state["tool_calls"])
        messages = list(state["messages"])

        for call in state["tool_calls"]:
            result = executor.execute(
                tool_name=call["name"],
                arguments=call["arguments"],
            )

            messages.append({
                "role": "tool",
                "tool_name": call["name"],
                "content": str(result),
            })

        return {
            "messages": messages,
            "tool_calls": [],
        }

    def route_after_agent(state: AgentState) -> str:
        if state["tool_calls"]:
            return "tools"

        return END
    
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)

    graph.add_edge(START, "agent")

    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge("tools", "agent")

    return graph.compile()

    # graph.add_state(
    #     START,
    #     state=AgentState(
    #         messages=[],
    #         tool_calls=[],
    #     )
    # )

    # graph.add_state(
    #     END,
    #     state=AgentState(
    #         messages=[],
    #         tool_calls=[],
    #     )
    # )

    # return graph