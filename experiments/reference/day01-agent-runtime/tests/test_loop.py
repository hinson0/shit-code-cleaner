from pathlib import Path

import pytest

from reference_impl.loop import (
    AgentLimitError,
    ModelTurn,
    ToolCall,
    run_agent,
)


class FakeModel:
    def __init__(self) -> None:
        self.calls = 0
        self.observation = None

    def generate(self, *, messages, tools) -> ModelTurn:
        self.calls += 1

        if self.calls == 1:
            return ModelTurn(
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name="read_file",
                        arguments={"path": "demo.py"},
                    )
                ]
            )

        self.observation = messages[-1]["content"]
        return ModelTurn(
            tool_calls=[],
            final_text="发现 demo.py 存在一个问题",
        )


def test_agent_executes_tool_and_continues(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text("def foo(): pass\n", encoding="utf-8")
    model = FakeModel()

    result = run_agent(
        model=model,
        messages=[],
        tools=[{"name": "read_file"}],
        repo_root=tmp_path,
        max_steps=4,
    )

    assert result == "发现 demo.py 存在一个问题"
    assert model.calls == 2
    assert model.observation == "def foo(): pass\n"


class NeverFinishModel:
    def generate(self, *, messages, tools) -> ModelTurn:
        return ModelTurn(
            tool_calls=[
                ToolCall(
                    id="call-loop",
                    name="read_file",
                    arguments={"path": "demo.py"},
                )
            ]
        )


def test_agent_stops_at_max_steps(tmp_path: Path) -> None:
    (tmp_path / "demo.py").write_text("pass\n", encoding="utf-8")

    with pytest.raises(AgentLimitError, match="max_steps=2"):
        run_agent(
            model=NeverFinishModel(),
            messages=[],
            tools=[{"name": "read_file"}],
            repo_root=tmp_path,
            max_steps=2,
        )
