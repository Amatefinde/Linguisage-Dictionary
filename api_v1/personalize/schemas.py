from pydantic import BaseModel


class RequestAddSense(BaseModel):
    word: str
    sense: str
    examples: list[str]
