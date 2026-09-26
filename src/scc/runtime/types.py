from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


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


class AgentModel(Protocol):
    def start(
        self,
        *,
        prompt: str,
        tools: Sequence[ToolSpec],
    ) -> ModelTurn: ...

    def resume(
        self,
        *,
        tool_results: Sequence[ToolResult],
        tools: Sequence[ToolSpec],
    ) -> ModelTurn: ...
