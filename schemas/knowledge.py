from pydantic import BaseModel


class KnowledgeAnswer(BaseModel):
    answer: str
    low_confidence: bool = False