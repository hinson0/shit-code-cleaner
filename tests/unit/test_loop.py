from pathlib import Path

from scc.runtime.loop import run_agent


class FakeModel:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, *, messages, tools):
        self.calls += 1

        if self.calls == 1:
            return {
                "tool_calls": [
                    {
                        "id": "call-1",
                        "name": "read_file",
                        "arguments": {
                            "path": "demo.py",
                        },
                    }
                ],
                "final_text": None,
            }

        return {
            "tool_calls": [],
            "final_text": "发现 demo.py 存在一个问题",
        }


def test_agent_executes_tool_and_continues(
    tmp_path: Path,
) -> None:
    target = tmp_path / "demo.py"
    target.write_text(
        "def foo(): pass\n",
        encoding="utf-8",
    )

    model = FakeModel()

    result = run_agent(
        model=model,
        messages=[],
        tools=["read_file"],
        repo_root=tmp_path,
        max_steps=4,
    )

    assert result == "发现 demo.py 存在一个问题"
    assert model.calls == 2
