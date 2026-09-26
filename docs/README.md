# docs 目录说明

`docs/` 保存 scc 的项目文档、学习记录和技术决策。产品实现放在 `src/`，这里不放可运行代码。

## 当前结构

```text
docs/
├── README.md
├── roadmap.md
├── progress.md
├── architecture.md
├── daily/
│   ├── _template.md
│   └── day01-agent-runtime.md
├── decisions/
│   └── _template.md
└── notes/
    └── agent-runtime.md
```

## 根目录文件

| 文件 | 作用 |
| --- | --- |
| `README.md` | 本文件。说明 `docs/` 中每类文档的职责和边界。 |
| `roadmap.md` | 学习与产品演进路线，只描述未来目标和阶段验收条件；是否完成以 `progress.md` 为准。 |
| `progress.md` | 当前事实状态：做到哪里、已完成什么、阻塞什么、最近如何验证、下一步做什么。 |
| `architecture.md` | 当前已经实现并核验过的架构、数据流、模块依赖和限制；不把未来规划写成现状。 |

## `daily/`

按学习日保存实际学习和实践记录。Day 编号按学习进度推进，不强绑定自然日期。

| 文件 | 作用 |
| --- | --- |
| `daily/_template.md` | 每日记录模板：目标、学习内容、实践改动、验收结果、问题与下一步。 |
| `daily/day01-agent-runtime.md` | Day 1 的实际记录，主题是 Agent Runtime 与最小 Tool Calling。 |

## `decisions/`

保存重要技术决策及其背景、取舍和代价。只有出现值得长期保留的架构或技术选择时才新增，不把普通实现细节都写成 ADR。

| 文件 | 作用 |
| --- | --- |
| `decisions/_template.md` | 技术决策模板，记录问题、最终选择、放弃项、理由、风险及重新评估条件。 |

## `notes/`

个人学习笔记。用于记录自己对 Agent 概念和工程实践的理解，不作为项目当前状态的权威来源。

| 文件 | 作用 |
| --- | --- |
| `notes/agent-runtime.md` | Agent Runtime 学习笔记，包括 LLM / Agent / Runtime / Tool 边界、Tool 安全边界和 Agent Loop 心智模型。 |

## 文档边界

- 看“以后要做什么” → `roadmap.md`
- 看“现在做到哪了” → `progress.md`
- 看“现在系统实际长什么样” → `architecture.md`
- 看“某一天具体学了和做了什么” → `daily/`
- 看“为什么做这个技术选择” → `decisions/`
- 看“个人怎么理解某个知识点” → `notes/`

新增、删除或调整 `docs/` 下的文档职责时，同步更新本文件。
