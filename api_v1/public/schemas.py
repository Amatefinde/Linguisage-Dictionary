from os.path import join
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_serializer, ConfigDict

from core import settings
from core.types import level_type

from core.schemas import BuildSoundUrlsMixin, BuildImgUrlMixin


class BaseWithConf(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WordImage(BaseWithConf, BuildImgUrlMixin):
    is_public: bool
    word_id: int = Field(exclude=True)
    id: int = Field(serialization_alias="f_image_id")
    img: str


class Example(BaseWithConf):
    id: int
    example: str
    html_example: Optional[str]
    sense_id: int = Field(exclude=True)


class Sense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int = Field(serialization_alias="f_sense_id")
    lvl: level_type | None = None
    short_cut: str | None = None
    word_id: int = Field(exclude=True)
    examples: List[Example] | None = None


class Alias(BaseWithConf):
    alias: str
    word_id: int
    id: int


class SWordResponse(BaseWithConf, BuildSoundUrlsMixin):
    word: str
    id: int = Field(serialization_alias="f_word_id")
    sound_uk: str | None = None
    sound_us: str | None = None
    word_images: List[WordImage]
    senses: List[Sense]
    aliases: List[Alias] = Field(exclude=True)


########################


class Word(BaseWithConf, BuildSoundUrlsMixin):
    word: str
    sound_us: str | None = None
    sound_uk: str | None = None
    id: int = Field(serialization_alias="f_word_id")
    word_images: List[WordImage] | None = None


class SPickedRandomSense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int = Field(serialization_alias="f_sense_id")
    lvl: level_type | None = None
    short_cut: str | None = None
    word_id: int = Field(exclude=True)
    word: Word
    examples: List[Example] | None = Field()


class SAdditionalRandomWord(BaseWithConf, BuildSoundUrlsMixin):
    word: str
    sound_us: str | None = None
    sound_uk: str | None = None
    id: int = Field(serialization_alias="f_word_id")


class SAdditionalRandomSense(BaseWithConf):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    id: int = Field(serialization_alias="f_sense_id")
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
