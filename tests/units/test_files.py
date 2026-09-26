from pathlib import Path

import pytest

from scc.tools.files import ToolError, read_file


def test_read_file(
    tmp_path: Path,
) -> None:
    (tmp_path / "a.py").write_text(
        "x = 1\n",
        encoding="utf-8",
    )

    assert (
        read_file(
            tmp_path,
            "a.py",
        )
        == "x = 1\n"
    )


def test_rejects_absolute_path(
    tmp_path: Path,
) -> None:
    target = tmp_path / "a.py"
    target.write_text(
        "x = 1\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ToolError,
        match="repository-relative",
    ):
        read_file(
            tmp_path,
            str(target.resolve()),
        )


def test_rejects_repository_escape(
    tmp_path: Path,
) -> None:
    outside = tmp_path.parent / "outside.py"
    outside.write_text(
        "secret = True\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ToolError,
        match="escapes repository",
    ):
        read_file(
            tmp_path,
            "../outside.py",
        )


def test_rejects_missing_file(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ToolError,
        match="cannot be resolved",
    ):
        read_file(
            tmp_path,
            "missing.py",
        )
