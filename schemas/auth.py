from pydantic import BaseModel


class SessionPayload(BaseModel):
    thread_id: str
    exp: int