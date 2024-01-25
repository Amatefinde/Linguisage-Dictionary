from pydantic import BaseModel, Field


# Create
class SBasePersonalizeSense(BaseModel):
    word: str
    definition: str
    part_of_speech: str | None = None
    examples: list[str] = Field(default_factory=lambda: [])


class SRequestAddPersonalizeSense(SBasePersonalizeSense):
    images_base64str: list[str] = Field(default_factory=lambda: [])


class SPersonalizeSense(SBasePersonalizeSense):
    image_filenames: list[str] = Field(default_factory=lambda: [])


# Update


class SRequestUpdatePersonalSense(BaseModel):
    definition: str | None = None
    part_of_speech: str | None = None
    examples: list[str] | None = None
    images_base64str: list[str] | None = None
