from typing import List, Optional

from pydantic import BaseModel, Field


class WordImage(BaseModel):
    is_public: bool
    word_id: int = Field(exclude=True)
    id: int
    img: str


class Example(BaseModel):
    html_example: Optional[str]
    sense_id: int = Field(exclude=True)
    example: str
    id: int


class Sense(BaseModel):
    lvl: Optional[str]
    short_cut: str
    word_id: int = Field(exclude=True)
    is_public: bool
    definition: str
    part_of_speech: str
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
