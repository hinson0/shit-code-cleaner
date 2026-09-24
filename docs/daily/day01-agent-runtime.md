# Day 01：Agent Runtime 与最小 Tool Calling

日期：2026-09-24

## 今晚目标

理解并能解释 LLM、Agent、Runtime、Tool 的职责边界；随后实现最小只读 Tool 和 Agent Loop。

阶段验收仍以实际代码为准：单 Agent 能请求 `read_file`，Runtime 执行工具并把结果回传模型，最终得到审查结果。

## 学习内容

- 区分普通 `input → LLM → output` 与 Agent 的多轮决策 / 行动 / 观察循环。
- 明确 LLM 负责决策，Runtime 负责调度和控制，Tool 负责真实 IO / 副作用。
- Tool Schema 是提供给模型的能力说明，不等于 Python Tool 实现本身。
- `repo_root` 属于 Runtime 的可信上下文，不应交给 LLM 决定。
- Runtime 需要 `max_steps` 等边界，不能把最终控制权交给模型。
- Tool 的可预期失败可以作为 Observation 回传模型，让 Agent 有机会修正。
- `tools/` 保存可复用能力；后续 MCP 只做协议适配，不复制 Tool。
- 今天手写 Agent Loop，是为了后续理解 LangGraph 如何把同一状态机工程化。

## 实践改动

- 已创建 `src/tools/`、`src/runtime/`、`src/agent/` 的模块骨架。
- 当前 `files.py`、`loop.py`、`reviewer.py` 均为空文件，尚不构成已实现能力。
- 单元测试代码由 ChatGPT 直接提供，用户不把学习时间投入测试设计。

## 验收结果

- 已核验当前源码文件存在但内容为空。
- Agent Loop：未实现，未验证。
- `read_file(repo_root: Path, path: str) -> str`：未实现，未验证。
- 单 Agent 实际 Tool Calling：未实现，未验证。
- 真实模型调用：未验证。
- 当前没有测试目录或可运行测试结果。

## 问题与下一步

下一步先实现 `read_file` 的最小安全边界，再实现有界 Agent Loop 和 Reviewer 角色。

Day 1 完成条件不以“看完理论”为准，而以最小 Agent Tool Calling 闭环实际跑通为准。
