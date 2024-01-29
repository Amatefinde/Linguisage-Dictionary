from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database.models import Word, Example, Sense, Alias, WordImage
from .schemas import SResponse


async def get_full_word(session: AsyncSession, alias: str):
    stmt = (
        select(Alias)
        .where(Alias.alias == alias)
        .options(
            joinedload(Alias.word),
            joinedload(Alias.word, Word.word_images),
            joinedload(Alias.word, Word.senses),
            joinedload(Alias.word, Word.senses, Sense.examples),
        )
    )
    row_response = await session.execute(stmt)
    if response := row_response.scalar():
        return SResponse.model_validate(response, from_attributes=True)
