from pathlib import Path


class ToolError(Exception):
    pass


def read_file(repo_root: Path, path: str) -> str:
    relative_path = Path(path)

    if relative_path.is_absolute():
        raise ToolError("path must be repository-relative")

    try:
        root = repo_root.resolve(strict=True)
        target = (root / relative_path).resolve(strict=True)
    except OSError as exc:
        raise ToolError("file cannot be resolved") from exc

    if not target.is_relative_to(root):
        raise ToolError("path escapes repository")

    if not target.is_file():
        raise ToolError("path is not a file")

    try:
        return target.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ToolError("file cannot be read as UTF-8") from exc
