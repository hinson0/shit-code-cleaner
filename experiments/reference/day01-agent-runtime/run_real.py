import os
from collections.abc import Sequence
from pathlib import Path

from reference.contracts import ModelTurn, ToolResult, ToolSpec
from reference.deepseek_model import DeepSeekReviewModel
from reference.runtime import run_agent


INSTRUCTIONS = """
You are a code review agent.
Review the requested source file for concrete correctness problems.
You MUST inspect the source with read_file before making findings.
Do not invent code you have not observed.
If no issue is found, say so explicitly.
Answer in concise Chinese.
""".strip()


class VerboseModel:
    def __init__(self, inner: DeepSeekReviewModel) -> None:
        self.inner = inner

    @staticmethod
    def _print_turn(turn: ModelTurn) -> None:
        for call in turn.tool_calls:
            print(f"[model -> tool] {call.name} {call.arguments}")
        if turn.final_text:
            print(f"[model -> final] {turn.final_text}")

    def start(self, *, prompt: str, tools: Sequence[ToolSpec]) -> ModelTurn:
        turn = self.inner.start(prompt=prompt, tools=tools)
        self._print_turn(turn)
        return turn

    def resume(
        self,
        *,
        tool_results: Sequence[ToolResult],
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        for result in tool_results:
            preview = result.output.replace("\n", "\\n")[:160]
            print(f"[tool -> model] {result.call_id} {preview}")
        turn = self.inner.resume(tool_results=tool_results, tools=tools)
        self._print_turn(turn)
        return turn


def main() -> None:
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise SystemExit("DEEPSEEK_API_KEY is required")

    root = Path(__file__).resolve().parent
    model_name = os.getenv("SCC_MODEL", "deepseek-flash")
    model = VerboseModel(
        DeepSeekReviewModel(model=model_name, instructions=INSTRUCTIONS)
    )
    result = run_agent(
        model=model,
        repo_root=root,
        prompt="Review sample/buggy.py.",
        max_steps=4,
    )
    print("\n=== result ===")
    print(result)


if __name__ == "__main__":
    main()
