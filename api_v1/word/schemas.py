from pydantic import BaseModel
from typing import Literal


class Meaning(BaseModel):
    meaning: str
    short_meaning: str | None
    common_form = str | None
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None
    examples: list[str] | None
    label: list[str] | None  # Example: Indian English, Transitive


class IdiomDefinition:
    definition: str
    examples: list[str] | None


class Idiom(BaseModel):
    idiom: str
    definitions: list[IdiomDefinition]


class PhrasalVerb(BaseModel):
    pass  # todo


class Word(BaseModel):
    word: str
    meaning: list[Meaning] | None
    phrasal_verbs: list[PhrasalVerb] | None
    idioms: list[Idiom] | None
