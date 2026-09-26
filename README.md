# shit-code-cleaner

`scc`（shit code cleaner）是一个用于学习和实践 Agent 工程的代码审查工具。

当前项目围绕一个可持续迭代的代码审查 Agent 展开，重点覆盖 Tool Calling、MCP、LangGraph、RAG、Memory、多 Agent 协作、评测和生产化。

## 环境

- Python 3.14
- uv

## 当前状态

项目仍处于 Day 01：Agent Runtime 与最小闭环。
实际完成情况以 `docs/progress.md` 为准，路线规划见 `docs/roadmap.md`。

## 开发

```powershell
uv sync
uv run pytest
uv run ruff check .
```

## 目录

- `src/scc/`：产品代码
- `tests/`：产品测试
- `docs/`：路线、进度、架构、每日记录和技术决策

## 原则

审查能力默认只读；参考实现通过不等于产品验收通过；FakeModel 测试通过不等于真实 LLM 联调完成。
