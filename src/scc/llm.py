import os
from collections.abc import Sequence

from dotenv import load_dotenv
from openai import OpenAI

from scc import runtime
from scc.reviewer import ModelTurn, ToolResult, ToolSpec

load_dotenv()


class DeepSeekModel:
    def __init__(self, *, model: str, instructions: str) -> None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("DEEPSEEK API KEY不存在")

        base_url = os.getenv("DEEPSEEK_BASE_URL")
        if not base_url:
            raise RuntimeError("DEEPSEEK BASE URL不存在")

        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model
        self._instructions = instructions
        self._messages: list[object] | None = None

    def start(self, *, prompt: str, tools: Sequence[ToolSpec]) -> ModelTurn:
        if self._messages is not None:
            raise RuntimeError("model session already started")

        self._messages = [
            {"role": "system", "content": self._instructions},
            {"role": "user", "content": prompt},
        ]

    def resume(
        self, *, tools: Sequence[ToolSpec], tool_results: Sequence[ToolResult]
    ) -> ModelTurn: ...
