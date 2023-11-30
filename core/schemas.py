from pydantic import BaseModel, ConfigDict
from typing import Literal


class SSense(BaseModel):
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    definition: str
    short_cut: str | None = None
    examples: list[str] | None = None
    row_examples: list[str] | None = None

    model_config = ConfigDict(from_attributes=True)


class IdiomDefinition(BaseModel):
    definition: str
    examples: list[str] | None


class Idiom(BaseModel):
    idiom: str
    definitions: list[IdiomDefinition]


class PhrasalVerb(BaseModel):
    pass  # todo


class SWord(BaseModel):
    word: str
    senses: list[SSense] = []
    phrasal_verbs: list[PhrasalVerb] = []
    idioms: list[Idiom] = []
