from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator

from core.schemas import BuildImgUrlMixin, BuildSoundUrlsMixin


class SImage(BuildImgUrlMixin, BaseModel):
    img: str
    is_public: bool
    id: int


class WordModel(BuildSoundUrlsMixin, BaseModel):
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
    word_images: list[SImage] | None = []
    sense_images: list[SImage]
    word: WordModel
    examples: list[ExampleModel]

    model_config = ConfigDict(from_attributes=True)


class SResponseSenses(BaseModel):
    senses: list[SResponseSense]
