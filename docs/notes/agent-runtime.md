## day1

| 东西    | 职责                       |
| ------- | -------------------------- |
| LLM     | 决策                       |
| Agent   | 面向一个目标使用模型和能力 |
| Runtime | 驱动整个执行过程           |
| Tool    | 真正操作外部世界           |
| MCP     | 后面学习的 Tool 接入协议   |

用户: review foo.py
LLM: 我没有 foo.py 的内容,我要调用: read_file(path='src/foo.py')
Runtime: 得到 llm 返回的 toolcall

```json
{
  "name": "read_file",
  "arguments": {
    "path": "src/foo.py"
  }
}
```

Runtime 才执行 content = read_file('src/foo.py')

然后得到 foo.py 的文件内容,把 content 喂给llm

因此,心智模型是:

LLM 负责:

- 我要干什么

Runtime:

- 怎么让他发生

Tool:

- 真正干活的

---

### filesystem boundary

- 文件系统边界.也就是说,一个 agent 不可以跨当前 repo 之外去做事情.(现阶段.以后是否会有超越 repo 边界的情况呢?)

### tool 的职责

arguments
↓
validate
↓
authorize => validate 管的是参数是否合理 => authorize 管的是当前是否有权限去干这件事情
↓
execute
↓
result

- 一个典型的 authorize 的场景

```python
target = (repo_root / path).resolve()

if target 不属于 repo_root:
    raise ToolError
```

###
