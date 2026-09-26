import argparse
from pathlib import Path

from reference_impl import ModelTurn, ToolCall, review_file


class DemoModel:
    """Deterministic model used only to expose the Agent Loop."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.calls = 0

    def generate(self, *, messages, tools) -> ModelTurn:
        self.calls += 1

        if self.calls == 1:
            return ModelTurn(
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name="read_file",
                        arguments={"path": self.path},
                    )
                ]
            )

        observation = next(
            message["content"]
            for message in reversed(messages)
            if message.get("role") == "tool"
        )
        preview = observation[:120].replace("\n", " ")
        return ModelTurn(
            tool_calls=[],
            final_text=f"reviewed after tool observation: {preview}",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("path")
    args = parser.parse_args()

    model = DemoModel(args.path)
    result = review_file(
        model=model,
        repo_root=args.repo_root,
        path=args.path,
    )

    print(result)
    print(f"model calls: {model.calls}")


if __name__ == "__main__":
    main()
