# 当前进度

> 只记录实际完成和核验过的状态，不根据规划推断完成。

## Day 01：已完成

- Python 版本已核验：`uv run python --version` → `Python 3.14.7`。
- Ruff 已核验：`uv run ruff check .` → `All checks passed!`。
- 离线测试已核验：`uv run pytest -q` → `12 passed in 0.09s`。
- 产品已具备最小 Agent Loop：DeepSeek 可请求 `read_file`，Runtime 执行后把 Tool Result 返回模型，再得到最终审查结论。
- `read_file` 限制在可信 `repo_root` 内，拒绝绝对路径、仓库逃逸和非法文件。
- Agent Loop 已覆盖协议错误、未知工具、非法参数、工具失败和 `max_steps` 耗尽。
- 真实 DeepSeek 联调已执行：自造缺陷样本被实际读取，并正确识别空列表索引异常及反向返回逻辑。
- 公共业务入口为 `src/scc/review.py`；CLI / API / Worker 后续都应复用该入口。

## 下一步：Day 02

实现 Tool Registry 与 Router，引入 `search_code`、`git_diff`，移除 Runtime 对具体工具名的硬编码分支，并执行 FakeModel + 真实 DeepSeek 多工具验收。
