from pydantic import BaseModel


class Confirmation(BaseModel):
    confirmed: bool