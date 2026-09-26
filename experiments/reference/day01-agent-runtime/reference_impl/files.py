from pathlib import Path
from typing import Any


class ToolError(Exception):
    """A predictable failure while executing a tool."""


READ_FILE_TOOL: dict[str, Any] = {
    "type": "function",
    "name": "read_file",
    "description": "Read a UTF-8 text file inside the repository.",
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
}


def read_file(repo_root: Path, path: str) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        raise ToolError("path must be repository-relative")

    root = repo_root.resolve()
    target = (root / candidate).resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ToolError("path escapes repository root") from exc

    if not target.is_file():
        raise ToolError("path is not a regular file")

    try:
        return target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolError("file is not valid UTF-8 text") from exc
