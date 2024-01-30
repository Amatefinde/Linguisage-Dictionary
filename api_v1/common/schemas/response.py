from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator
from os.path import join
from core import settings


class SWordImage(BaseModel):
    img: str
    word_id: int = Field(exclude=True)
    is_public: bool
    id: int

    @field_validator("img")
    @classmethod
    def make_url(cls, img: str):
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_images', img)}"

    model_config = ConfigDict(from_attributes=True)


class WordModel(BaseModel):
    word: str
    sound_us: str
    sound_uk: str
    id: int


class ExampleModel(BaseModel):
    html_example: str | None = None
    example: str
    sense_id: int = Field(exclude=True)
    id: int


class SResponseSense(BaseModel):
    id: int
    short_cut: str | None = None
    part_of_speech: str | None = None
    word_id: int = Field(exclude=True)
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None
    is_public: bool
    definition: str | None = None
    word_images: list[SWordImage] | None = []
    word: WordModel
    examples: list[ExampleModel]

    model_config = ConfigDict(from_attributes=True)


class SResponseSenses(BaseModel):
    senses: list[SResponseSense]
