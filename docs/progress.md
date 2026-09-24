# 当前进度

> 只记录实际完成和核验过的状态，不根据规划推断完成。

- 当前阶段：Day 1 — Agent Runtime 与最小 Tool Calling，尚未完成。
- 已完成：Day 1 核心概念学习；已明确 LLM / Runtime / Tool 边界、Tool Schema、Observation、终止与执行预算等概念；已创建 `src/tools/`、`src/runtime/`、`src/agent/` 空模块骨架。
- 当前目标：实现 `read_file(repo_root: Path, path: str) -> str`，再实现有界 Agent Loop，使单 Agent 能完成一次只读文件审查。
- 阻塞 / 风险：`files.py`、`loop.py`、`reviewer.py` 当前为空；没有可运行产品行为。尚未建立固定效果评测基线。
- 最近验证：2026-09-24 核验源码树；上述三个核心文件均为空。Agent Loop、Tool Calling、测试和真实模型调用均未验证。
- 下一步：实现最小 `read_file` Tool；测试由 ChatGPT 提供，学习重点放在 Runtime 和 Agent Loop。
- 当天记录：`daily/day01-agent-runtime.md`。
- 文档分工：项目 daily / progress / decisions / roadmap / architecture 由 ChatGPT 按条件维护；个人 `docs/notes/` 由用户自愿维护。
