import os
from pathlib import Path

from dotenv import load_dotenv

from scc.llm import DeepSeekModel
from scc.reviewer import (
    REVIEWER_INSTRUCTIONS,
    review,
)


def main() -> None:
    load_dotenv()

    api_key = os.environ["DEEPSEEK_API_KEY"]

    # 得到model
    model = DeepSeekModel(
        api_key=api_key,
        instructions=REVIEWER_INSTRUCTIONS,
    )

    # review文件
    result = review(
        Path.cwd(),
        "tests/fixtures/day01_buggy.py",
        model=model,
        max_steps=4,
    )

    print(result)


if __name__ == "__main__":
    main()
