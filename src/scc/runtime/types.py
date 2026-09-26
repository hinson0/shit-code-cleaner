from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolCall:
    call_id: str
    name: str
    arguments: dict[str, object]


@dataclass(frozen=True, slots=True)
class ToolResult:
    call_id: str
    output: str


@dataclass(frozen=True, slots=True)
class ModelTurn:
    tool_calls: tuple[ToolCall, ...] = ()
    final_text: str | None = None


type ToolSpec = dict[str, object]
