from pydantic import BaseModel, ConfigDict
from typing import Literal
from enum import Enum


class SDictionarySense(BaseModel):
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    definition: str
    short_cut: str | None = None
    examples: list[str] | None = []
    row_examples: list[str] | None = []

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
    alias: str
    part_of_speech: str | None = None
    sound_uk_url: str | None = None
    sound_us_url: str | None = None
    senses: list[SDictionarySense] = []
    phrasal_verbs: list[SPhrasalVerb] = []
    idioms: list[SIdiom] = []


class SWordDictionaryLink(BaseModel):
    word: str
    link: str
