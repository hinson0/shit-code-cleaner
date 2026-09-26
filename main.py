from pathlib import Path

from scc.llm import DeepSeekModel
from scc.runtime.loop import run_agent

INSTRUCTIONS = """
You are a code review agent.
Review the requested source file for concrete correctness problems.
You MUST inspect the source with read_file before making findings.
Do not invent code you have not observed.
If no issue is found, say so explicitly.
Answer in concise Chinese.
""".strip()


def main() -> None:
    root = Path(__file__).parent.resolve()

    model = DeepSeekModel(
        model="deepseek-flash",
        instructions=INSTRUCTIONS,
    )

    result = run_agent(
        model=model,
        repo_root=root,
        prompt="Review src/scc/tools/files.py",
        max_steps=4,
    )

    print(result)


if __name__ == "__main__":
    main()
