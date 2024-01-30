from os.path import join
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator, field_validator

from core import settings


class WordImage(BaseModel):
    is_public: bool
    word_id: int = Field(exclude=True)
    id: int
    img: str

    @field_validator("img")
    @classmethod
    def make_url(cls, img: str):
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_images', img)}"


class Example(BaseModel):
    html_example: Optional[str]
    sense_id: int = Field(exclude=True)
    example: str
    id: int


class Sense(BaseModel):
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None
    short_cut: str | None = None
    word_id: int = Field(exclude=True)
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int
    examples: List[Example]


class Word(BaseModel):
    word: str
    id: int
    sound_uk: str
    sound_us: str
    word_images: List[WordImage]
    senses: List[Sense]


class SResponse(BaseModel):
    word_id: int = Field(exclude=True)
    id: int = Field(exclude=True)
    alias: str
    word: Word
