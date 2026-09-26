# Day 01 reference: Agent Runtime

这是隔离参考答案，不属于 `src/scc/` 产品实现，也不能代替产品验收。

## 结构

- `reference/contracts.py`: Model / Tool 调用契约。
- `reference/tools.py`: 只读 `read_file`，限制在 repo_root 内。
- `reference/runtime.py`: 有界 Agent Loop；Day 01 只认识 `read_file`。
- `reference/deepseek_model.py`: DeepSeek Chat Completions 适配器。
- `tests/`: FakeModel 离线测试。
- `sample/buggy.py`: 真实 LLM 联调用自造样本。
- `run_real.py`: 显示 model -> tool -> model -> final 的联调轨迹。

## Day 01 的 Provider 约束

DeepSeek 使用 OpenAI-compatible SDK，但本日不启用 thinking mode。
这样可以只关注 Agent Loop、Tool Calling 和 Tool Result 回传；
思考模式下的 reasoning_content 回传留到后续再学。

## 离线测试

PowerShell：

```powershell
cd experiments/reference/day01-agent-runtime
uv run --no-project --with pytest python -m pytest -q
```

## 真实模型联调

不要把 key 写进仓库：

```powershell
$env:DEEPSEEK_API_KEY="你的 key"
$env:SCC_MODEL="deepseek-flash"
uv run --no-project --with openai python run_real.py
```

验收时必须看到三段：

1. `[model -> tool] read_file ...`
2. `[tool -> model] ...`，内容来自 `sample/buggy.py`
3. `[model -> final] ...`，指出实际读到的代码问题

FakeModel 测试通过只证明 Runtime 控制流；真实 DeepSeek 跑通才证明 tool calling 联调完成。
