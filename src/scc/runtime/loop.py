from pathlib import Path

from scc.reviewer import AgentModel, ToolResult, ToolSpec
from scc.tools.files import ToolError, read_file


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


def run_agent(
    *,
    model: AgentModel,
    repo_root: Path,
    prompt: str,
    max_steps: int = 4,
):
    if max_steps < 1:
        raise ValueError("max steps 参数不能小于1")

    turn = model.start(prompt=prompt, tools=[READ_FILE_TOOL])

    for step in range(max_steps):
        if not turn.tool_calls:
            if not turn.final_text:
                raise AgentProtocolError("没有tool_calls，又没有final_text")
            return turn.final_text

        results = []

        for tool_call in turn.tool_calls:
            if tool_call.name != "read_file":
                tool_result = ToolResult(
                    call_id=tool_call.call_id,
                    output="工具名字不是read_file",
                )
                results.append(tool_result)

            # 检查tool call的path参数是否合法
            path = tool_call.arguments.get("path")
            if not isinstance(path, str):
                tool_result = ToolResult(
                    call_id=tool_call.call_id, output="参数path不是一个字符串"
                )
                results.append(tool_result)

            # 执行read_file
            try:
                content = read_file(repo_root, path)
                tool_result = ToolResult(call_id=tool_call.call_id, output=content)
            except ToolError:
                tool_result = ToolResult(
                    call_id=tool_call.call_id, output="读取文件失败"
                )
                results.append(tool_result)

            turn = model.resume(tools=[READ_FILE_TOOL], tool_results=results)

    raise StepLimitExceeded
