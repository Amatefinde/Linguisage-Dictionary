from pydantic import BaseModel, ConfigDict
from typing import Literal


class SSense(BaseModel):
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    definition: str
    short_cut: str | None = None
    examples: list[str] | None = []
    row_examples: list[str] | None = []
    images: list[str] = []

    model_config = ConfigDict(from_attributes=True)


class SIdiomDefinition(BaseModel):
    definition: str
    examples: list[str] | None


class SIdiom(BaseModel):
    idiom: str
    definitions: list[SIdiomDefinition]


class SPhrasalVerb(BaseModel):
    pass  # todo


class SWord(BaseModel):
    word: str
    senses: list[SSense] = []
    phrasal_verbs: list[SPhrasalVerb] = []
    idioms: list[SIdiom] = []


class SWordDictionaryLink(BaseModel):
    word: str
    link: str
