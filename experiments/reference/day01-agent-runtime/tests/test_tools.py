from pathlib import Path

import pytest
from reference.tools import ToolError, read_file


def test_read_file_returns_content(tmp_path: Path) -> None:
    (tmp_path / "demo.py").write_text("x = 1\n", encoding="utf-8")
    assert read_file(tmp_path, "demo.py") == "x = 1\n"


def test_read_file_rejects_parent_escape(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.py"
    outside.write_text("secret = True\n", encoding="utf-8")

    with pytest.raises(ToolError, match="escapes repository root"):
        read_file(tmp_path, "../outside.py")


def test_read_file_rejects_absolute_path(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text("x = 1\n", encoding="utf-8")

    with pytest.raises(ToolError, match="repository-relative"):
        read_file(tmp_path, str(target.resolve()))


def test_read_file_rejects_directory(tmp_path: Path) -> None:
    (tmp_path / "pkg").mkdir()

    with pytest.raises(ToolError, match="not a readable file"):
        read_file(tmp_path, "pkg")


def test_read_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ToolError, match="not a readable file"):
        read_file(tmp_path, "missing.py")
