import json
from collections.abc import Awaitable, Callable
from typing import TypeVar

from pydantic import BaseModel

from core.llm import chat_llm
from schemas.common import Confirmation

CONFIRM_PROMPT = "Did the user just confirm they want to proceed (yes/go ahead/etc)? Message: {message}"

T = TypeVar("T")


async def with_retry(call: Callable[[], Awaitable[T]], attempts: int = 2) -> T:
    """Groq's structured-output mode occasionally echoes the schema instead of an instance - retry once."""
    for attempt in range(attempts):
        try:
            return await call()
        except Exception:
            if attempt == attempts - 1:
                raise


def json_shape_example(schema_cls: type[BaseModel]) -> str:
    return json.dumps(
        {name: f"<{info['type']}>" for name, info in schema_cls.model_json_schema()["properties"].items()}
    )


def merge_fields(existing: BaseModel, new: BaseModel) -> BaseModel:
    data = existing.model_dump()
    for key, value in new.model_dump().items():
        if value is not None:
            data[key] = value
    return type(existing)(**data)


def first_missing_field(fields: BaseModel) -> str | None:
    for name in fields.model_fields:
        if getattr(fields, name) is None:
            return name
    return None


async def is_confirmed(message: str) -> bool:
    llm = chat_llm.with_structured_output(Confirmation, method="json_schema")
    result = await with_retry(lambda: llm.ainvoke(CONFIRM_PROMPT.format(message=message)))
    return result.confirmed