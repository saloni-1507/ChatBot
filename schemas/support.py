from pydantic import BaseModel


class SupportResolution(BaseModel):
    answer: str
    resolved: bool