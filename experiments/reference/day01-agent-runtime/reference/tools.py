from pathlib import Path


class ToolError(RuntimeError):
    pass


def read_file(repo_root: Path, path: str) -> str:
    root = repo_root.resolve()
    if not root.is_dir():
        raise ToolError(f"repo_root is not a directory: {repo_root}")

    relative = Path(path)
    if relative.is_absolute():
        raise ToolError("path must be repository-relative")

    target = (root / relative).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ToolError("path escapes repository root") from exc

    if not target.is_file():
        raise ToolError(f"not a readable file: {path}")

    try:
        return target.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ToolError(f"failed to read {path}: {exc}") from exc
