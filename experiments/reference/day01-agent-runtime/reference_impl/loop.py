from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol

from .files import ToolError, read_file


type Message = dict[str, Any]
type ToolSchema = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ModelTurn:
    tool_calls: list[ToolCall]
    final_text: str | None = None


class Model(Protocol):
    def generate(
        self,
        *,
        messages: list[Message],
        tools: list[ToolSchema],
    ) -> ModelTurn: ...


class AgentRuntimeError(RuntimeError):
    pass


class AgentLimitError(AgentRuntimeError):
    pass


def _execute_tool(repo_root: Path, call: ToolCall) -> str:
    if call.name != "read_file":
        return f"ERROR: unknown tool: {call.name}"

    path = call.arguments.get("path")
    if not isinstance(path, str):
        return "ERROR: read_file.path must be a string"

    try:
        return read_file(repo_root, path)
    except ToolError as exc:
        return f"ERROR: {exc}"


def run_agent(
    *,
    model: Model,
    messages: list[Message],
    tools: list[ToolSchema],
    repo_root: Path,
    max_steps: int = 8,
) -> str:
    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")

    history = list(messages)

    for _step in range(max_steps):
        turn = model.generate(messages=history, tools=tools)

        if not turn.tool_calls:
            if turn.final_text is None:
                raise AgentRuntimeError(
                    "model returned neither tool calls nor final text"
                )
            return turn.final_text

        history.append(
            {
                "role": "assistant",
                "tool_calls": [asdict(call) for call in turn.tool_calls],
            }
        )

        for call in turn.tool_calls:
            result = _execute_tool(repo_root, call)
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": call.name,
                    "content": result,
                }
            )

    raise AgentLimitError(f"agent exceeded max_steps={max_steps}")
