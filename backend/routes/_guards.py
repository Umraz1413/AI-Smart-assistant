from fastapi import HTTPException

from config import settings


def enforce_max_length(text: str, field_name: str = "text") -> None:
    if len(text) > settings.MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=413,
            detail=(
                f"{field_name} is too long ({len(text)} chars). "
                f"Limit is {settings.MAX_INPUT_CHARS} characters."
            ),
        )
