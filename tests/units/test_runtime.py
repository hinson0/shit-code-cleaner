from collections.abc import Sequence
from pathlib import Path

import pytest

from scc.runtime.loop import (
    AgentProtocolError,
    AgentStepLimitError,
    run_agent,
)
from scc.runtime.types import (
    ModelTurn,
    ToolCall,
    ToolResult,
    ToolSpec,
)


class FakeModel:
    def __init__(
        self,
        *turns: ModelTurn,
    ) -> None:
        self._turns = list(turns)
        self.received_results: list[tuple[ToolResult, ...]] = []

    def _next(self) -> ModelTurn:
        if not self._turns:
            raise AssertionError("FakeModel has no remaining turns")

        return self._turns.pop(0)

    def start(
        self,
        *,
        prompt: str,
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        return self._next()

    def resume(
        self,
        *,
        tool_results: Sequence[ToolResult],
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        self.received_results.append(tuple(tool_results))

        return self._next()


def test_direct_final(
    tmp_path: Path,
) -> None:
    model = FakeModel(ModelTurn(final_text="ok"))

    result = run_agent(
        model=model,
        repo_root=tmp_path,
        prompt="review",
    )

    assert result == "ok"


def test_tool_then_final(
    tmp_path: Path,
) -> None:
    (tmp_path / "a.py").write_text(
        "x = 1\n",
        encoding="utf-8",
    )

    model = FakeModel(
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-1",
                    name="read_file",
                    arguments={
                        "path": "a.py",
                    },
                ),
            )
        ),
        ModelTurn(final_text="done"),
    )

    result = run_agent(
        model=model,
        repo_root=tmp_path,
        prompt="review",
    )

    assert result == "done"

    assert model.received_results == [
        (
            ToolResult(
                call_id="call-1",
                output="x = 1\n",
            ),
        )
    ]


def test_unknown_tool_becomes_tool_result(
    tmp_path: Path,
) -> None:
    model = FakeModel(
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-1",
                    name="delete_everything",
                    arguments={},
                ),
            )
        ),
        ModelTurn(final_text="cannot use that tool"),
    )

    result = run_agent(
        model=model,
        repo_root=tmp_path,
        prompt="review",
    )

    assert result == "cannot use that tool"

    assert model.received_results[0][0].output.startswith("ERROR: unknown tool")


def test_invalid_arguments_become_tool_result(
    tmp_path: Path,
) -> None:
    model = FakeModel(
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-1",
                    name="read_file",
                    arguments={
                        "path": 123,
                    },
                ),
            )
        ),
        ModelTurn(final_text="invalid arguments"),
    )

    run_agent(
        model=model,
        repo_root=tmp_path,
        prompt="review",
    )

    assert model.received_results[0][0] == ToolResult(
        call_id="call-1",
        output="ERROR: path must be a string",
    )


def test_tool_error_is_returned_to_model(
    tmp_path: Path,
) -> None:
    model = FakeModel(
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-1",
                    name="read_file",
                    arguments={
                        "path": "../outside.py",
                    },
                ),
            )
        ),
        ModelTurn(final_text="cannot review"),
    )

    result = run_agent(
        model=model,
        repo_root=tmp_path,
        prompt="review",
    )

    assert result == "cannot review"

    assert model.received_results[0][0].output.startswith("ERROR:")


def test_protocol_error(
    tmp_path: Path,
) -> None:
    model = FakeModel(ModelTurn())

    with pytest.raises(AgentProtocolError):
        run_agent(
            model=model,
            repo_root=tmp_path,
            prompt="review",
        )


def test_rejects_invalid_max_steps(
    tmp_path: Path,
) -> None:
    model = FakeModel(ModelTurn(final_text="unused"))

    with pytest.raises(
        ValueError,
        match="max_steps",
    ):
        run_agent(
            model=model,
            repo_root=tmp_path,
            prompt="review",
            max_steps=0,
        )


def test_step_limit_stops_before_unconsumable_tool_call(
    tmp_path: Path,
) -> None:
    (tmp_path / "a.py").write_text(
        "x = 1\n",
        encoding="utf-8",
    )

    model = FakeModel(
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-1",
                    name="read_file",
                    arguments={
                        "path": "a.py",
                    },
                ),
            )
        ),
        ModelTurn(
            tool_calls=(
                ToolCall(
                    call_id="call-2",
                    name="read_file",
                    arguments={
                        "path": "a.py",
                    },
                ),
            )
        ),
    )

    with pytest.raises(
        AgentStepLimitError,
        match="max_steps=2",
    ):
        run_agent(
            model=model,
            repo_root=tmp_path,
            prompt="review",
            max_steps=2,
        )

    assert len(model.received_results) == 1

    assert model.received_results[0][0].call_id == "call-1"
