# Day 01：最小 Agent Loop

日期：2026-09-23；状态：阻塞，未完成。

## 今晚目标
在现有仓库交付 CLI → review → reviewer → loop → read_file → JSON 报告。
仅审查用户指定的 UTF-8 文件；工具只读、仓库内、限定大小。
Python 3.14，uv 管理；不接 MCP、RAG、多 Agent、数据库。

## 学习内容
模型提出工具调用，Runtime 校验并执行，再按 call_id 回传结果。
结构校验不等于结论正确；离线测试不等于真实模型验收。

## 实践改动
pyproject.toml：Python 范围限制为 >=3.14,<3.15，声明依赖、开发组与 Ruff 配置。
已生成 uv.lock、.venv；.gitignore 增加 .scc/。
新增 tests/conftest.py 和 16 项文件边界测试；测试禁网，临时文件位于 .scc/。
scc 命令及打包配置只是预配置，产品代码未落地。

## 验收结果
uv --version → 0.7.6；uv python find 3.14 --no-python-downloads → 已安装 3.14.2。
uv sync --python 3.14 --no-install-project → 成功，安装 22 个包，不含项目自身。
首次测试 → 16 errors，原因是 .scc/ 父目录不存在；补 pytest_configure 自动创建。
重跑 uv run --no-sync pytest tests/unit/test_files.py --tb=short → 16 failed。
失败均为 ModuleNotFoundError: No module named 'scc'；实现尚未写入，不能算通过。

## 问题与下一步
产品代码写入被工具安全检查拦截，后续目录核验确认 src/ 不存在。
构建、CLI、真实模型调用：未验证。缺固定模型评测基线。
先解决写入阻塞，再实现文件工具、转绿测试，继续 Agent Loop；本次未提交或推送。

## 收尾核验
uv run --no-sync python --version → Python 3.14.2。
uv lock --check → 通过。
uv run --no-sync ruff format tests → 格式化 1 个文件；ruff check tests → 通过。
git diff --check → 通过。
uv run --no-sync pytest tests/unit/test_files.py --tb=line → 16 failed，仍全部缺 scc 模块。
发现 AGENTS.md 有非本次写入的工作区改动，已重新读取，未覆盖。
