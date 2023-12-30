import time

from sqlalchemy.orm import joinedload, selectinload
from loguru import logger
from core.database.models import Word, Image, Example, Sense, RowExample, Alias
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.schemas import SWord, SSense
from .schemas import WordDTO, SenseDTO, ImageDTO
from typing import Iterable


async def get_word_by_id(
    session: AsyncSession,
    word_id: int,
) -> Word | None:
    return await session.get(Word, word_id)


async def get_word_by_name(
    session: AsyncSession,
    name: str,
) -> Word | None:
    stmt = select(Word).where(Word.word == name)
    return await session.scalar(stmt)


def get_db_images_from_s_sense(sense: SSense) -> list[Image]:
    images = []
    for image in sense.images:
        images.append(Image(img=image))
    return images


def get_examples_from_s_sense(sense: SSense) -> list[Example]:
    examples = []
    for example in sense.examples:
        examples.append(Example(example=example))
    return examples


def get_row_examples_from_s_sense(sense: SSense) -> list[RowExample]:
    row_examples = []
    for row_example in sense.row_examples:
        row_examples.append(RowExample(row_example=row_example))
    return row_examples


def get_db_senses_from_s_word(word: SWord) -> list[Sense]:
    senses = []
    for sense in word.senses:
        db_sense = Sense(
            lvl=sense.lvl,
            definition=sense.definition,
            short_cut=sense.short_cut,
            images=get_db_images_from_s_sense(sense),
            examples=get_examples_from_s_sense(sense),
            row_examples=get_row_examples_from_s_sense(sense),
        )
        senses.append(db_sense)
    return senses


async def add(
    session: AsyncSession,
    word: SWord,
) -> Word | None:
    db_word: Word = await get_word_by_name(session, word.word)

    if not db_word:
        db_word = Word(word=word.word)
        db_word.aliases = [Alias(alias=word.word)]
        db_word.senses = get_db_senses_from_s_word(word)
        session.add(db_word)
        await session.commit()
        return db_word
    else:
        senses: list[Sense] = get_db_senses_from_s_word(word)
        for sense in senses:
            sense.word_id = db_word.id
            session.add(sense)
            await session.commit()


async def get_all_word_data(session: AsyncSession, alias: str):
    stmt = (
        select(Alias)
        .where(Alias.alias == alias)
        .options(joinedload(Alias.word).selectinload(Word.senses).selectinload(Sense.examples))
        .options(joinedload(Alias.word).selectinload(Word.senses).selectinload(Sense.row_examples))
        .options(joinedload(Alias.word).selectinload(Word.senses).selectinload(Sense.images))
    )
    db_response = await session.execute(stmt)
    result = db_response.scalar()
    if result:
        return WordDTO.model_validate(result.word)


async def add_alias_to_word(session: AsyncSession, alias: str, word: str) -> Alias | None:
    stmt = select(Alias).where(Alias.alias == alias)
    db_alias = await session.scalar(stmt)
    db_word = await get_word_by_name(session, word)
    if not db_word:
        return
    if not db_alias:
        db_alias = Alias(alias=alias, word=db_word)
        session.add(db_alias)
        await session.commit()
        return db_alias


def _filter_images_for_sense(sense: SenseDTO, collection: Iterable[int]) -> SenseDTO:
    collection = set(collection)
    sense = sense.model_copy()
    sense.images = [img for img in sense.images if img.id in collection]
    return sense


async def get_sense_with_word_and_images_by_sense_id(
    session: AsyncSession, sense_id: int, images_id: list[int] = None
) -> SenseDTO | None:
    start = time.time()
    stmt = (
        select(Sense)
        .options(
            selectinload(Sense.images),
            selectinload(Sense.examples),
            selectinload(Sense.row_examples),
            selectinload(Sense.word),
        )
        .where(Sense.id == sense_id)
    )

    sense_db = await session.scalar(stmt)
    if sense_db:
        logger.info(f"Time for get only one sense with images and example: {time.time()-start}s")
        sense_dto = SenseDTO.model_validate(sense_db)
        logger.info(f"Time for get only one sense with images and example: {time.time()-start}s")
        return _filter_images_for_sense(sense_dto, images_id)


async def get_many_senses_with_word_and_images_by_sense_id(
    session: AsyncSession, senses_id: list[int], images_id: list[int] = None
) -> list[SenseDTO] | None:
    stmt = (
        select(Sense)
        .options(
            joinedload(Sense.images),
            joinedload(Sense.examples),
            joinedload(Sense.row_examples),
            joinedload(Sense.word),
        )
        .filter(Sense.id.in_(senses_id))
    )

    row_response = await session.execute(stmt)
    senses_db = row_response.scalars().unique().all()
    if senses_db:
        senses_dto: list[SenseDTO] = []
        for sense in senses_db:
            sense_dto = SenseDTO.model_validate(sense)
            sense_dto_with_filtered_images = _filter_images_for_sense(sense_dto, images_id)
            senses_dto.append(sense_dto_with_filtered_images)
        return senses_dto


async def get_image_by_id(session: AsyncSession, image_id: int) -> ImageDTO | None:
    image_db = await session.get(Image, image_id)
    if image_db:
        return ImageDTO.model_validate(image_db)
