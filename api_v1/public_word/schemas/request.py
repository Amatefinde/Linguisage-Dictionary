from pydantic import BaseModel


class SRequestSense(BaseModel):
    sense_id: int
    word_image_ids: set[int] | None = []
    sense_image_ids: set[int] | None = []


class SRequestManySense(BaseModel):
    senses: list[SRequestSense]
