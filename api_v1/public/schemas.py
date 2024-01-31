from os.path import join
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

from core import settings
from core.types import level_type


class BaseWithConf(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WordImage(BaseWithConf):
    is_public: bool
    word_id: int = Field(exclude=True)
    id: int
    img: str

    @field_validator("img")
    @classmethod
    def make_url(cls, img: str):
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_images', img)}"


class Example(BaseWithConf):
    id: int
    example: str
    html_example: Optional[str]
    sense_id: int = Field(exclude=True)


class Sense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int
    lvl: level_type | None = None
    short_cut: str | None = None
    word_id: int = Field(exclude=True)
    examples: List[Example] | None = None


class Alias(BaseWithConf):
    alias: str
    word_id: int
    id: int


class SWordResponse(BaseWithConf):
    word: str
    id: int
    sound_uk: str | None = None
    sound_us: str | None = None
    word_images: List[WordImage]
    senses: List[Sense]
    aliases: List[Alias] = Field(exclude=True)


########################


class Word(BaseWithConf):
    word: str
    sound_us: str | None = None
    sound_uk: str | None = None
    id: int
    word_images: List[WordImage] | None = None


class SPickedRandomSense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int
    lvl: level_type | None = None
    short_cut: str | None = None
    word_id: int = Field(exclude=True)
    word: Word
    examples: List[Example] | None = Field()


class SAdditionalRandomWord(BaseWithConf):
    word: str
    sound_us: str | None = None
    sound_uk: str | None = None
    id: int


class SAdditionalRandomSense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int
    lvl: level_type | None = None
    short_cut: str | None = Field(default=None, exclude=True)
    word_id: int = Field(exclude=True)
    word: SAdditionalRandomWord


class SAdditionalPOSs(BaseWithConf):
    noun: list[SAdditionalRandomSense] = Field(default_factory=list)
    verb: list[SAdditionalRandomSense] = Field(default_factory=list)
    adjective: list[SAdditionalRandomSense] = Field(default_factory=list)
    adverb: list[SAdditionalRandomSense] = Field(default_factory=list)


class SRandomSensesResponse(BaseWithConf):
    senses: list[SPickedRandomSense]
    additional: SAdditionalPOSs
