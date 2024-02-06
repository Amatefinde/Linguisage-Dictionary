from os.path import join
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer

from core import settings


class BuildSoundUrlsMixin(BaseModel):
    @field_serializer("sound_uk", check_fields=False)
    def build_sound_uk_url(self, sound_uk: str | None):
        if sound_uk is None:
            return None
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_audio', sound_uk)}"

    @field_serializer("sound_us", check_fields=False)
    def build_sound_us_url(self, sound_us: str | None):
        if sound_us is None:
            return None
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_audio', sound_us)}"


class BuildImgUrlMixin(BaseModel):
    @field_serializer("img", check_fields=False)
    def make_url(self, img: str):
        domain = f"{settings.SERVER_PROTOCOL}://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
        return f"{domain}/{join('static','word_images', img)}"


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
