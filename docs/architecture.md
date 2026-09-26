# 当前架构

仅记录已实现且核验过的内容；未来规划见 `roadmap.md`。

## Day 01 已实现架构

```text
调用方
  ↓
src/scc/review.py
  ↓
src/scc/runtime/loop.py
  ├──→ src/scc/llm.py → DeepSeek API
  │        ↑                │
  │        └── Tool Result ─┘
  │
  └──→ src/scc/tools/files.py → 仓库文件
```

## 模块职责

- `review.py`：当前业务入口，构造代码审查请求并调用 Runtime。
- `runtime/types.py`：定义 `ToolCall`、`ToolResult`、`ModelTurn`、`AgentModel` 等边界类型。
- `runtime/loop.py`：驱动模型轮次、执行工具、回传结果、处理协议错误与步数上限。
- `llm.py`：DeepSeek 的 OpenAI-compatible Chat Completions 协议适配。
- `tools/files.py`：提供仓库内只读文件访问，负责路径边界和读取错误。

## 当前数据流

1. 调用方通过 `review()` 指定仓库根目录和目标文件。
2. Runtime 把任务和 `read_file` schema 交给 DeepSeek。
3. DeepSeek 返回 Tool Call。
4. Runtime 校验工具名和参数，并调用 `read_file`。
5. Tool Result 使用对应 `call_id` 回传模型。
6. 模型返回最终文本后 Runtime 结束。

## 已知限制

- 当前只有 `read_file` 一个工具，工具路由仍硬编码；Day 02 处理 Registry / Router。
- 当前审查结果仍是文本，不是结构化 `ReviewReport`。
- 当前没有 MCP、LangGraph、RAG、Memory 或多 Agent。
- Runtime 状态只存在当前进程内，没有 Checkpoint。
