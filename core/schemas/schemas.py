from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class CoreSSense(BaseModel):
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    part_of_speech: str | None = None
    definition: str | None = None
    short_cut: str | None = None
    examples: list[str] | None = None
    html_examples: list[str] | None = None
    images: list[str] | None = None


class CoreSWord(BaseModel):
    word: str
    alias: str | None = None
    sound_uk: str | None = None
    sound_us: str | None = None
    senses: list[CoreSSense] | None = None
    images: list[str] | None = None
