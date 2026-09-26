# Day 01：Agent Runtime 与最小闭环

日期：2026-09-26

## 今晚目标
修正 Day 01 参考实现中不符合 Python 3.14 约束的废弃 typing 别名，并重新验证离线测试；本次不把 Day 01 标记为完成。

## 学习内容
`typing.Sequence` 是对 `collections.abc.Sequence` 的废弃别名；Python 3.14 代码直接使用 `collections.abc.Sequence`。保留 `typing.Protocol`。

## 实践改动
在 `experiments/reference/day01-agent-runtime/` 的 5 个 Python 文件中，把 `typing.Sequence` 改为 `collections.abc.Sequence`。没有修改 `src/scc/` 产品代码。

## 验收结果
- `uv run python --version` → `Python 3.14.7`。
- 从仓库根执行 `uv run pytest experiments/reference/day01-agent-runtime/tests -q` → 收集失败：`ModuleNotFoundError: reference`，原因是参考目录未进入导入路径。
- 在参考实现目录执行 `uv run --no-project --python 3.14 --with pytest python -m pytest -q` → `9 passed in 0.09s`。
- 搜索 `from typing import Sequence` → 0 个匹配。
- 补充仓库根 `README.md` 后，`uv run ruff check .` 已能成功构建当前项目；随后失败于 `ruff` 未安装（`program not found`）。

## 问题与下一步
真实 LLM 联调尚未验收。当前参考实现仍是 OpenAI Responses API，而项目模型约束是 DeepSeek-only；在做 Day 01 真实联调前必须先替换适配器和运行说明。
