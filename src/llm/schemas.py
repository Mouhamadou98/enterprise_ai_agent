from dataclasses import dataclass, field


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict
    id: str | None = None


@dataclass
class LLMResponse:
    content: str | None = None
    tool_calls: ToolCall = field(default_factory=list)