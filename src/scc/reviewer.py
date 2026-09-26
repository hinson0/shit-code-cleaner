from collections.abc import Sequence
from typing import Protocol

from scc.runtime.types import ModelTurn, ToolResult, ToolSpec


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
        tools: Sequence[ToolSpec],
        tool_results: Sequence[ToolResult],
    ) -> ModelTurn: ...
