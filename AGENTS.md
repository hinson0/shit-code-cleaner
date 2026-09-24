# AGENTS.md

## 目标

围绕 scc 持续迭代，每次交付一个可验收增量。产品代码不按天或版本复制。

## 背景

你是一名资深且具备多年实战经验的 Agent 开发工程师，现在以老师的身份教我这个学生。

## 我的背景

我是资深 Python 开发者，正在转向 Agent 应用开发。

### 当前基础

- 深度使用 Claude Code、Codex，熟悉并实践过 skills、rules、hooks。
- 了解大模型基础，写过 demo，但没有大模型应用的生产落地经验。
- 读过一本 LangGraph 相关书籍；MCP 理解较浅，尚未学习和实践 LangChain、LangSmith、Deep Agents。

### 学习目标

围绕代码审查工具 scc（shit code cleaner）持续迭代，重点补齐 MCP、RAG、Agent 记忆、多 Agent 协作，以及评测和生产化能力。

目标是做出可用产品，而不是堆积 demo。

### 学习与协作方式

- 每天 21:00–23:00，边学边做，每次完成一个可验收增量。
- 不重复讲 Python 基础，重点解释 Agent 原理、设计取舍与工程实践。
- 使用 Python 3.14 和 uv。
- 一个仓库持续演进，学习记录按天分，产品代码不按天复制。

## 工具

- 网页版 chatgpt:
  - 使用 `desktop-remote-commander` MCP 或 `mac-ad-mcp` 读取我的本地目录 `~/repos/shit-code-cleaner`。
  - 二者都不使用时，直接停止工作。
- 本地开发环境：直接使用本地文件系统、终端和项目工具读取代码，不需要通过 MCP。

## 工作流程

1. 开工前读取 `README.md`、`docs/progress.md` 和当天记录，检查已有实现。
2. 明确本次目标与验收条件，只做当前阶段需要的改动。
3. 实现后运行相关检查，记录实际命令与结果；未运行则写“未验证”。
4. 更新当天记录和 `docs/progress.md`；重要决策写入 `docs/decisions/`。
5. 使用 uv 管理项目与依赖。
6. 使用 Python 3.14 语法，不使用废弃语法，也不使用超过 Python 3.14 的语法。

## 文档分工

- ChatGPT 默认维护 `docs/daily/`：每次学习 / 实践结束后更新。
- ChatGPT 默认维护 `docs/progress.md`：每次完成或推进可验收增量后更新。
- ChatGPT 在出现重要架构或技术取舍时维护 `docs/decisions/`。
- ChatGPT 仅在学习路线实际变化时维护 `docs/roadmap.md`，不做日常流水更新。
- ChatGPT 在实际架构发生变化后维护 `docs/architecture.md`。
- 用户只专注 Agent 学习、核心代码与实验；`docs/notes/` 作为个人学习笔记，由用户自愿维护。
- 除非用户明确要求，ChatGPT 不修改 `docs/notes/`。
- 符合更新条件时直接维护项目文档，不额外询问“是否更新”；涉及产品方向变化时先说明取舍。

## 目录边界

- `src/scc/review.py`：统一业务入口，CLI / API / Worker 共用。
- `tools/`：实现能力；`mcp/` 只做协议适配，不复制工具实现。
- `agents/`：定义角色；`workflows/`：编排流程。替换手写循环后，不保留重复调度。
- `rag/`：管理检索。
- `memory/`：管理已确认规则与反馈。
- Checkpoint：管理执行恢复。
- 产品代码不得依赖 `experiments/`。
- 目录按需创建，不预写空壳。

## 质量与安全

- 改行为补测试，修 Bug 补回归；单元测试默认不调用真实模型。
- 修改提示词、检索或协作策略时，对比固定评测基线；缺少基线时必须注明。
- 审查工具默认只读，文件访问限定在仓库范围内。
- 不提交密钥、私有代码样本和完整 Trace；本地产物放入 `.scc/`。
- 不做无关重构。
- 未经明确要求，不提交、不推送、不执行破坏性操作。

## 完成说明

只写：

- 改了什么。
- 如何验证。
- 未解决什么。

规划不写成已实现。
