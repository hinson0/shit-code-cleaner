# Day 01 参考实现：Agent Runtime

这是一份独立参考答案，不是 `src/scc/` 的产品代码。

包含：

- `reference_impl/files.py`：只读 `read_file` Tool 与 Tool Schema。
- `reference_impl/loop.py`：有界 Agent Loop、Tool 调度、Observation 回传。
- `reference_impl/reviewer.py`：最薄 Reviewer Agent。
- `demo.py`：不用真实模型也能观察两轮 Agent Loop。
- `tests/`：参考实现自己的离线测试。

运行测试：

```powershell
uv run pytest experiments/reference/day01-agent-runtime/tests -q
```

运行演示：

```powershell
uv run python experiments/reference/day01-agent-runtime/demo.py . README.md
```

重点看 `loop.py`：Decision → Act → Observation → 再 Decision。
