# 当前进度

> 只记录实际完成和核验过的状态，不根据规划推断完成。

## Day 01：进行中

- 项目解释器约束已核验：`.python-version` 为 3.14，实际 `uv run python --version` 为 Python 3.14.7。
- Day 01 隔离参考实现已移除 `typing.Sequence` 废弃别名，改用 `collections.abc.Sequence`。
- 参考实现离线测试已在 Python 3.14 下通过：9 passed。
- 仓库根 `README.md` 已补齐，`uv` 项目构建不再因缺失 README 失败；当前 `ruff` 尚未安装。
- Day 01 尚未验收：真实 LLM 的 tool calling 联调未执行。
- 当前遗留：参考实现仍使用 OpenAI 适配器，不符合项目 DeepSeek-only 模型约束，需先修正后再做真实联调。
