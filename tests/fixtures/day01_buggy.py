def first_or_none(items: list[str]) -> str | None:
    if not items:
        return items[0]

    return None
