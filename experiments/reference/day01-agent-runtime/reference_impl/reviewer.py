from pathlib import Path

from .files import READ_FILE_TOOL
from .loop import Model, run_agent


REVIEWER_PROMPT = """\
You are a code review agent.

Review the requested source file for concrete correctness problems.
Inspect the source with read_file before making findings.
Do not invent code you have not observed.
If no issue is found, say so explicitly.
"""


def review_file(
    *,
    model: Model,
    repo_root: Path,
    path: str,
    max_steps: int = 8,
) -> str:
    messages = [
        {"role": "system", "content": REVIEWER_PROMPT},
        {"role": "user", "content": f"Review this file: {path}"},
    ]

    return run_agent(
        model=model,
        messages=messages,
        tools=[READ_FILE_TOOL],
        repo_root=repo_root,
        max_steps=max_steps,
    )
