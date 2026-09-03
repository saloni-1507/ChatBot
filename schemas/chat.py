from typing import Annotated

from pydantic import BaseModel, StringConstraints


class ChatRequest(BaseModel):
    message: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    image_b64: str | None = None


class ChatResponse(BaseModel):
    reply: str
    token: str