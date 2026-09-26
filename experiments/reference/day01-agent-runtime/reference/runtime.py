import json
from collections.abc import Sequence
from pathlib import Path

from .contracts import AgentModel, ModelTurn, ToolCall, ToolResult, ToolSpec
from .tools import ToolError, read_file


class AgentProtocolError(RuntimeError):
    pass


class StepLimitExceeded(RuntimeError):
    pass


READ_FILE_TOOL: ToolSpec = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a UTF-8 source file inside the repository.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Repository-relative file path.",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
}


def _error(call_id: str, message: str) -> ToolResult:
    payload = json.dumps({"ok": False, "error": message}, ensure_ascii=False)
    return ToolResult(call_id=call_id, output=payload)


def execute_call(repo_root: Path, call: ToolCall) -> ToolResult:
    if call.name != "read_file":
        return _error(call.call_id, f"unknown tool: {call.name}")

    path = call.arguments.get("path")
    if not isinstance(path, str):
        return _error(call.call_id, "read_file.path must be a string")

    try:
        content = read_file(repo_root, path)
    except ToolError as exc:
        return _error(call.call_id, str(exc))

    return ToolResult(call_id=call.call_id, output=content)


def _terminal_text(turn: ModelTurn) -> str | None:
    if turn.tool_calls:
        return None
    if turn.final_text is None or not turn.final_text.strip():
        raise AgentProtocolError("model returned neither tool call nor final text")
    return turn.final_text


def run_agent(
    *,
    model: AgentModel,
    repo_root: Path,
    prompt: str,
    max_steps: int = 4,
    tools: Sequence[ToolSpec] = (READ_FILE_TOOL,),
) -> str:
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")

    turn = model.start(prompt=prompt, tools=tools)
    for step in range(1, max_steps + 1):
        final_text = _terminal_text(turn)
        if final_text is not None:
            return final_text

        if step == max_steps:
            break

        results = tuple(execute_call(repo_root, call) for call in turn.tool_calls)
        turn = model.resume(tool_results=results, tools=tools)

    raise StepLimitExceeded(f"agent exceeded max_steps={max_steps}")
