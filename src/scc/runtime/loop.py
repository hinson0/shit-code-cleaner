from pathlib import Path

from scc.runtime.types import AgentModel, ToolCall, ToolResult, ToolSpec
from scc.tools.files import ToolError, read_file


class AgentProtocolError(RuntimeError):
    pass


class AgentStepLimitError(RuntimeError):
    pass


READ_FILE_TOOL: ToolSpec = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read one UTF-8 source file inside the repository.",
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


def _execute_tool(repo_root: Path, call: ToolCall) -> ToolResult:
    if call.name != "read_file":
        return ToolResult(
            call_id=call.call_id,
            output=f"ERROR: unknown tool {call.name!r}",
        )

    if set(call.arguments) != {"path"}:
        return ToolResult(
            call_id=call.call_id,
            output="ERROR: read_file expects exactly one argument: path",
        )

    path = call.arguments["path"]
    if not isinstance(path, str):
        return ToolResult(
            call_id=call.call_id,
            output="ERROR: path must be a string",
        )

    try:
        content = read_file(repo_root, path)
    except ToolError as exc:
        return ToolResult(
            call_id=call.call_id,
            output=f"ERROR: {exc}",
        )

    return ToolResult(
        call_id=call.call_id,
        output=content,
    )


def run_agent(
    *,
    model: AgentModel,
    repo_root: Path,
    prompt: str,
    max_steps: int = 4,
) -> str:
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")

    turn = model.start(
        prompt=prompt,
        tools=[READ_FILE_TOOL],
    )

    for step in range(max_steps):
        if turn.tool_calls:
            if step == max_steps - 1:
                break

            results = tuple(_execute_tool(repo_root, call) for call in turn.tool_calls)

            turn = model.resume(
                tool_results=results,
                tools=[READ_FILE_TOOL],
            )
            continue

        if turn.final_text:
            return turn.final_text

        raise AgentProtocolError("model returned neither tool_calls nor final_text")

    raise AgentStepLimitError(f"agent exceeded max_steps={max_steps}")
