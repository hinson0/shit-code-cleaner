import os
from collections.abc import Sequence

from dotenv import load_dotenv
from openai import OpenAI

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

        return self._request(tools)

    def resume(
        self,
        *,
        tool_results: Sequence[ToolResult],
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        if self._messages is None:
            raise RuntimeError("model session has not started")

        self._messages.extend(
            {
                "role": "tool",
                "tool_call_id": result.call_id,
                "content": result.output,
            }
            for result in tool_results
        )
        return self._request(tools)

    def _request(self, tools: Sequence[ToolSpec]) -> ModelTurn:
        assert self._messages is not None
        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages,
            tools=list(tools),
            tool_choice="auto",
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
        message = response.choices[0].message
        self._messages.append(message)
        return self._to_turn(message)

    @staticmethod
    def _to_turn(message: object) -> ModelTurn:
        calls: list[ToolCall] = []
        for tool_call in message.tool_calls or ():
            arguments = json.loads(tool_call.function.arguments)
            if not isinstance(arguments, dict):
                raise RuntimeError("tool arguments must decode to an object")
            calls.append(
                ToolCall(
                    call_id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=arguments,
                )
            )

        content = message.content
        text = content.strip() if isinstance(content, str) and content.strip() else None
        return ModelTurn(tool_calls=tuple(calls), final_text=text)
