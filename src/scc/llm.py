import json
from collections.abc import Sequence
from typing import Any

from openai import OpenAI

from scc.runtime.types import ModelTurn, ToolCall, ToolResult, ToolSpec


class DeepSeekResponseError(RuntimeError):
    pass


class DeepSeekModel:
    def __init__(
        self,
        *,
        api_key: str,
        instructions: str,
        model: str = "deepseek-flash",
        base_url: str = "https://api.deepseek.com",
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self._model = model
        self._instructions = instructions
        self._messages: list[dict[str, Any]] | None = None

    def start(
        self,
        *,
        prompt: str,
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        if self._messages is not None:
            raise RuntimeError("model session already started")

        self._messages = [
            {
                "role": "system",
                "content": self._instructions,
            },
            {
                "role": "user",
                "content": prompt,
            },
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

    def _request(
        self,
        tools: Sequence[ToolSpec],
    ) -> ModelTurn:
        if self._messages is None:
            raise RuntimeError("model session has not started")

        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages,
            tools=list(tools),
            tool_choice="auto",
            stream=False,
            extra_body={
                "thinking": {
                    "type": "disabled",
                }
            },
        )

        if not response.choices:
            raise DeepSeekResponseError("DeepSeek returned no choices")

        message = response.choices[0].message

        self._messages.append(self._assistant_message(message))

        return self._to_turn(message)

    @staticmethod
    def _assistant_message(
        message: Any,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "role": "assistant",
            "content": message.content,
        }

        if message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in message.tool_calls
            ]

        return result

    @staticmethod
    def _to_turn(
        message: Any,
    ) -> ModelTurn:
        calls: list[ToolCall] = []

        for call in message.tool_calls or ():
            try:
                arguments = json.loads(call.function.arguments)
            except json.JSONDecodeError as exc:
                raise DeepSeekResponseError(
                    "tool arguments are not valid JSON"
                ) from exc

            if not isinstance(arguments, dict):
                raise DeepSeekResponseError("tool arguments must be a JSON object")

            calls.append(
                ToolCall(
                    call_id=call.id,
                    name=call.function.name,
                    arguments=arguments,
                )
            )

        content = message.content

        final_text = (
            content.strip() if isinstance(content, str) and content.strip() else None
        )

        return ModelTurn(
            tool_calls=tuple(calls),
            final_text=final_text,
        )
