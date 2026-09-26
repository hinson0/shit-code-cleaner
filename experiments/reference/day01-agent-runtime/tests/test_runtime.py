from collections import deque
from collections.abc import Sequence
from pathlib import Path

import pytest

from reference.contracts import ModelTurn, ToolCall, ToolResult, ToolSpec
from reference.runtime import StepLimitExceeded, run_agent


class FakeModel:
    def __init__(self, turns: list[ModelTurn]) -> None:
        self.turns = deque(turns)
        self.seen_results: list[ToolResult] = []
        self.start_calls = 0
        self.resume_calls = 0

    def start(self, *, prompt: str, tools: Sequence[ToolSpec]) -> ModelTurn:
        self.start_calls += 1
        assert prompt
        assert tools[0]["function"]["name"] == "read_file"
        return self.turns.popleft()

    def resume(
        self,
        *,
        tool_results: Sequence[ToolResult],
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        self.resume_calls += 1
        self.seen_results.extend(tool_results)
        return self.turns.popleft()


def read_call(path: str) -> ToolCall:
    return ToolCall(
        call_id="call-1",
        name="read_file",
        arguments={"path": path},
    )


def test_agent_executes_tool_then_returns_final_text(tmp_path: Path) -> None:
    (tmp_path / "demo.py").write_text("x = 1\n", encoding="utf-8")
    model = FakeModel(
        [
            ModelTurn(tool_calls=(read_call("demo.py"),)),
            ModelTurn(final_text="发现一个问题"),
        ]
    )

    result = run_agent(model=model, repo_root=tmp_path, prompt="review demo.py")

    assert result == "发现一个问题"
    assert model.start_calls == 1
    assert model.resume_calls == 1
    assert model.seen_results[0].output == "x = 1\n"


def test_tool_error_is_returned_to_model(tmp_path: Path) -> None:
    model = FakeModel(
        [
            ModelTurn(tool_calls=(read_call("../outside.py"),)),
            ModelTurn(final_text="读取失败，无法审查"),
        ]
    )

    result = run_agent(model=model, repo_root=tmp_path, prompt="review")

    assert result == "读取失败，无法审查"
    assert '"ok": false' in model.seen_results[0].output
    assert "escapes repository root" in model.seen_results[0].output


def test_unknown_tool_is_returned_as_error(tmp_path: Path) -> None:
    model = FakeModel(
        [
            ModelTurn(
                tool_calls=(ToolCall("call-1", "delete_file", {"path": "x"}),)
            ),
            ModelTurn(final_text="工具不可用"),
        ]
    )

    assert run_agent(model=model, repo_root=tmp_path, prompt="review") == "工具不可用"
    assert "unknown tool: delete_file" in model.seen_results[0].output


def test_agent_stops_at_step_limit_before_next_tool_execution(tmp_path: Path) -> None:
    (tmp_path / "demo.py").write_text("x = 1\n", encoding="utf-8")
    model = FakeModel(
        [
            ModelTurn(tool_calls=(read_call("demo.py"),)),
            ModelTurn(tool_calls=(read_call("demo.py"),)),
        ]
    )

    with pytest.raises(StepLimitExceeded, match="max_steps=2"):
        run_agent(
            model=model,
            repo_root=tmp_path,
            prompt="review",
            max_steps=2,
        )

    assert model.resume_calls == 1
    assert len(model.seen_results) == 1
