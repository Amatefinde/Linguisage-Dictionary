from typing import Literal

from loguru import logger
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.database.models import Word, Example, Sense, Alias, WordImage
from core.types import level_type, main_pos
from .schemas import (
    SWordResponse,
    SRandomSensesResponse,
    SPickedRandomSense,
    SAdditionalRandomSense,
)


async def get_full_word(session: AsyncSession, alias: str):
    stmt = (
        select(Word)
        .options(
            selectinload(Word.aliases),
            selectinload(Word.word_images),
            selectinload(Word.senses.and_(Sense.is_public)),
            selectinload(Word.senses, Sense.examples),
        )
        .join(Alias)
        .where(Alias.alias == alias)
    )
    row_response = await session.execute(stmt)
    if response := row_response.scalar():
        return SWordResponse.model_validate(response, from_attributes=True)


async def get_random_senses(
    session: AsyncSession,
    amount: int,
    lvl: list[level_type] | None = None,
    pos: list[main_pos] | None = None,
    black_list_sense_ids: list[int] | None = None,
    load_examples_and_images: bool = False,
) -> list[SPickedRandomSense] | list[SAdditionalRandomSense]:
    stmt = (
        select(Sense)
        .where(Sense.is_public)
        .options(joinedload(Sense.word))
        .order_by(func.random())
        .limit(amount)
    )
    if load_examples_and_images:
        stmt = stmt.options(
            selectinload(Sense.examples),
            selectinload(Sense.word, Word.word_images),
        )
    if lvl:
        stmt = stmt.where(Sense.lvl.in_(lvl))
    if pos:
        stmt = stmt.where(Sense.part_of_speech.in_(pos))
    if black_list_sense_ids:
        stmt = stmt.where(Sense.id.notin_(black_list_sense_ids))
    row_response = await session.execute(stmt)
    db_senses = row_response.scalars().all()
    if load_examples_and_images:
        return [SPickedRandomSense.model_validate(sense) for sense in db_senses]
    else:
        return [SAdditionalRandomSense.model_validate(sense) for sense in db_senses]
