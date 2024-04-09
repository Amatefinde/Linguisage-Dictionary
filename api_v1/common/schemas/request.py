from pydantic import BaseModel

from core.types import level_type


class SRequestSense(BaseModel):
    sense_id: int
    word_image_ids: set[int] | None = []
    sense_image_ids: set[int] | None = []


class SClause(BaseModel):
    search: str | None = None
    lvl: list[level_type] | None = None


class SRequestManySenseWithContent(BaseModel):
    senses: list[SRequestSense]
    clauses: SClause | None = None

