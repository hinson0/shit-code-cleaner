# scc — shit code cleaner

逐步构建的 AI 代码审查工具：读取 Git diff，定位问题，输出审查报告。

当前为文档初始化包，不含程序实现；已有代码进度以核验后填写的记录为准。

## 迭代路线
单 Agent → MCP → 工作流与评测 → Code RAG → Memory → 多 Agent → PR 接入。

每天 21:00–23:00：30 分钟学习、80 分钟实践、10 分钟总结。

## 目录约定
```text
src/scc/       产品代码，按阶段创建
tests/        软件正确性测试
evals/        审查效果评测
experiments/  隔离实验
docs/         路线、进度、架构、每日记录与决策
.scc/         本地产物，不提交
```

## 开发入口
先读 [协作规则](AGENTS.md) 和 [当前进度](docs/progress.md)。
按 [路线](docs/roadmap.md) 迭代，用 [每日模板](docs/daily/_template.md) 记录验收结果。

## 运行
待最小闭环跑通后，补充已验证的安装、配置和审查命令。
