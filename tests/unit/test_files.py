import os

import pytest


def test_read_file_is_read_only(tmp_path):
    from scc.tools.files import read_file

    source = tmp_path / "example.py"
    source.write_text("# 中文\nanswer = 42\n", encoding="utf-8")
    before = source.read_bytes()
    assert read_file(tmp_path, "example.py") == before.decode("utf-8")
    assert source.read_bytes() == before


@pytest.mark.parametrize(
    "path", ["../outside.py", "/etc/passwd", ".env", ".git/config", "key.pem", ""]
)
def test_reject_unsafe_paths(tmp_path, path):
    from scc.tools.files import ToolError, read_file

    with pytest.raises(ToolError):
        read_file(tmp_path, path)


@pytest.mark.parametrize("kind", ["file", "directory"])
def test_reject_symlinks(tmp_path, kind):
    from scc.tools.files import ToolError, read_file

    actual = tmp_path / "actual"
    actual.mkdir()
    (actual / "example.py").write_text("secret = 1\n")
    link = tmp_path / "link"
    link.symlink_to(actual if kind == "directory" else actual / "example.py")
    with pytest.raises(ToolError):
        read_file(tmp_path, "link/example.py" if kind == "directory" else "link")


@pytest.mark.parametrize("data", [b"x" * 9, b"\xff", b"\x00"])
def test_reject_large_or_non_text_files(tmp_path, data):
    from scc.tools.files import ToolError, read_file

    (tmp_path / "example.py").write_bytes(data)
    with pytest.raises(ToolError):
        read_file(tmp_path, "example.py", max_bytes=8)


@pytest.mark.parametrize("kind", ["missing", "directory", "fifo"])
def test_reject_non_regular_files(tmp_path, kind):
    from scc.tools.files import ToolError, read_file

    path = tmp_path / "example.py"
    if kind == "directory":
        path.mkdir()
    elif kind == "fifo":
        os.mkfifo(path)
    with pytest.raises(ToolError):
        read_file(tmp_path, "example.py")


def test_accept_exact_size_and_empty_file(tmp_path):
    from scc.tools.files import read_file

    path = tmp_path / "example.py"
    path.write_bytes(b"12345678")
    assert read_file(tmp_path, "example.py", max_bytes=8) == "12345678"
    path.write_bytes(b"")
    assert read_file(tmp_path, "example.py") == ""
