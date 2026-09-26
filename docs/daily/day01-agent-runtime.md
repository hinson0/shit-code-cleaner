# Day 01：Agent Runtime 与最小闭环

日期：2026-09-26

## 今日目标

从零实现并验收最小代码审查 Agent 闭环：

```text
用户请求 → DeepSeek → read_file Tool Call → Runtime 执行 → Tool Result → DeepSeek → 审查结论
```

## 理解与设计

- LLM 负责推理和决定是否调用工具，不直接执行文件操作。
- Runtime 负责 Agent Loop、工具执行、结果回传、协议错误和步数上限。
- Tool 负责一个受控真实能力；`repo_root` 由程序持有，模型只能提供仓库相对路径。
- Tool Calling 与 Tool Execution 是两件事；`tool_call_id` 用来关联请求和结果。
- `max_steps` 是模型轮次上限；最后一轮仍请求工具时不再执行无法被后续模型消费的调用。

## 实践改动

- 业务入口统一为 `src/scc/review.py`。
- `src/scc/runtime/types.py` 定义 Model / Tool 的边界数据结构与 Protocol。
- `src/scc/runtime/loop.py` 实现单工具 Agent Loop、协议错误和步数限制。
- `src/scc/tools/files.py` 实现只读 `read_file`，拒绝绝对路径、仓库逃逸和非法文件。
- `src/scc/llm.py` 实现 DeepSeek Chat Completions Tool Calling 适配器，Day 01 使用非思考模式。
- `scripts/day01_live.py` 用自造缺陷样本执行真实 DeepSeek 联调。
- 单测覆盖直接结束、一次工具调用、未知工具、非法参数、工具失败、协议错误、非法 max_steps 和步数耗尽。

## 验收结果

- `uv run python --version` → `Python 3.14.7`。
- `uv run ruff check .` → `All checks passed!`。
- `uv run pytest -q` → `12 passed in 0.09s`。
- 真实 DeepSeek 联调成功：模型读取 `tests/fixtures/day01_buggy.py` 后，指出空列表分支访问 `items[0]` 会触发 `IndexError`，且非空列表错误返回 `None`。
- FakeModel、静态检查和真实 LLM 联调分别记录，没有互相替代。

## 今日结论

Day 01 验收通过。已经建立最小 Agent Runtime 心智模型和真实 Tool Calling 闭环。

## 下一步

Day 02：Tool Calling、Registry 与 Router。把当前只支持 `read_file` 的硬编码调度替换为统一工具注册与路由。
