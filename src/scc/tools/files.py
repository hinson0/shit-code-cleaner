from pathlib import Path


class ToolError(Exception):
    pass


def read_file(repo_root: Path, path: str) -> str:
    p = Path(path)

    # Agent 只能传仓库相对路径
    if p.is_absolute():
        raise ToolError("path需要是一个绝对路径 而不是一个相对路径")

    # 得到仓库真实路径
    root = repo_root.resolve()

    # repo_root + Agent 给出的 path
    target = (root / path).resolve()

    # 防止：
    #
    # ../secret
    # ../../etc/passwd
    #
    # resolve 后逃出仓库
    if repo_root not in p.parents:
        raise ToolError("你必须要在仓库里面 不可以逃出仓库外")

    # 不读目录等东西
    if not target.is_fifo():
        raise ToolError

    # Tool 真正执行外部操作的地方
    return target.read_text(encoding="utf-8")
