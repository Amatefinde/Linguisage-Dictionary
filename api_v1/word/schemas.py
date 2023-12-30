from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator
from core.config import settings


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExamplesDTO(BaseDTO):
    example: str


class RowExamplesDTO(BaseDTO):
    row_example: str


class ImageDTO(BaseDTO):
    id: int
    img: str

    @field_validator("img", mode="before")
    def add_prefix(cls, value):
        return f"{settings.SERVER_HOST}:{settings.SERVER_PORT}/{value}"


class WordForSenseDTO(BaseDTO):
    id: int
    word: str


class SenseDTO(BaseDTO):
    id: int
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    short_cut: str | None = None
    definition: str
    examples: list[ExamplesDTO] = None
    row_examples: list[RowExamplesDTO] = None
    images: list[ImageDTO] = None

    word: WordForSenseDTO | None = None


class WordDTO(BaseDTO):
    id: int
    word: str
    senses: list[SenseDTO]


class RequestSenseWithImages(BaseModel):
    sense_id: int
    images_ids: list[int]


class RequestSensesWithImages(BaseModel):
    senses: list[RequestSenseWithImages]
