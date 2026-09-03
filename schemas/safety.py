from pydantic import BaseModel


class ModerationVerdict(BaseModel):
    violation: bool
    category: str | None = None
    rationale: str