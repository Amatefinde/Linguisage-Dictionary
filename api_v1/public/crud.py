from typing import Literal

from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.database.models import Word, Example, Sense, Alias, WordImage
from .schemas import SResponse


async def get_full_word(session: AsyncSession, alias: str):
    stmt = (
        select(Alias)
        .where(Alias.alias == alias)
        .options(
            joinedload(Alias.word),
            joinedload(Alias.word, Word.word_images),
            joinedload(Alias.word, Word.senses.and_(Sense.is_public)),
            joinedload(Alias.word, Word.senses, Sense.examples),
        )
    )
    row_response = await session.execute(stmt)
    if response := row_response.scalar():
        return SResponse.model_validate(response, from_attributes=True)


async def get_random_words(
    session: AsyncSession,
    amount: int,
    lvl: list[Literal["A1", "A2", "B1", "B2", "C1", "C2"]] | None,
):
    stmt = (
        select(Sense)
        .where(Sense.is_public)
        .options(
            joinedload(Sense.word),
            joinedload(Sense.word, Word.word_images),
            joinedload(Sense.examples),
        )
        .order_by(func.random())
        .limit(amount)
    )
    if lvl:
        stmt = stmt.where(Sense.lvl.in_(lvl))
    row_response = await session.execute(stmt)
    if response := row_response.unique().scalars().all():
        return response
