from pathlib import Path

import pytest

from scc.tools.files import ToolError, read_file


def test_read_file_returns_content(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text("print('hello')\n", encoding="utf-8")

    result = read_file(tmp_path, "demo.py")

    assert result == "print('hello')\n"


def test_read_file_rejects_path_outside_repo(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.py"
    outside.write_text("secret = True\n", encoding="utf-8")

    with pytest.raises(ToolError):
        read_file(tmp_path, "../outside.py")


def test_read_file_rejects_absolute_path(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text("print('hello')\n", encoding="utf-8")

    with pytest.raises(ToolError):
        read_file(tmp_path, str(target))


def test_read_file_rejects_directory(tmp_path: Path) -> None:
    directory = tmp_path / "pkg"
    directory.mkdir()

    with pytest.raises(ToolError):
        read_file(tmp_path, "pkg")
