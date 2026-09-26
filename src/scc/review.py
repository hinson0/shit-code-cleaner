from pathlib import Path

from scc.runtime.loop import run_agent
from scc.runtime.types import AgentModel

REVIEWER_INSTRUCTIONS = """
你是一个代码审查 Agent。

审查用户指定的源文件，查找明确、具体的正确性问题。

在给出任何问题之前，必须先使用 `read_file` 读取并检查指定的源文件。

不要臆测或编造你没有实际查看过的代码。

如果无法读取或检查该文件，明确说明本次代码审查无法完成。

如果没有发现明确的问题，也要明确说明未发现问题。

用中文回复
""".strip()


def review(
    repo_root: Path,
    path: str,
    *,
    model: AgentModel,
    max_steps: int = 4,
) -> str:
    prompt = f"Review this repository file: {path}"

    return run_agent(
        model=model,
        repo_root=repo_root,
        prompt=prompt,
        max_steps=max_steps,
    )
