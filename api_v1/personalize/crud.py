import os
from os.path import join
from typing import Sequence

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core import settings
from core.database.models import Sense, Word, Example, Alias, HtmlExample, SenseImage
from api_v1.public.crud import get_word_by_alias
from .schemas import SPersonalizeSense, SRequestUpdatePersonalSense


async def get_db_sense_with_all_field(session: AsyncSession, sense_id: int) -> Sense | None:
    db_sense = await session.get(
        Sense,
        sense_id,
        options=[
            selectinload(Sense.sense_images),
            selectinload(Sense.html_examples),
            selectinload(Sense.examples),
        ],
    )
    return db_sense


async def add_sense(
    session: AsyncSession,
    personalize_sense: SPersonalizeSense,
):
    db_word = await get_word_by_alias(session, personalize_sense.word)
    if not db_word:
        db_word = Word(word=personalize_sense.word)
        session.add(db_word)
        db_alias = Alias(alias=personalize_sense.word, word=db_word)
        session.add(db_alias)
    db_examples = [Example(example=example) for example in personalize_sense.examples]
    db_html_examples = [HtmlExample(html_example=example) for example in personalize_sense.examples]
    db_images = [SenseImage(img=img, is_public=False) for img in personalize_sense.image_filenames]
    db_sense = Sense(
        word=db_word,
        part_of_speech=personalize_sense.part_of_speech,
        definition=personalize_sense.definition,
        is_public=False,
        examples=db_examples,
        html_examples=db_html_examples,
        sense_images=db_images,
    )
    session.add(db_sense)
    await session.commit()
    await session.close()

    return await get_db_sense_with_all_field(session, db_sense.id)


async def delete_sense_images(session: AsyncSession, images: Sequence[SenseImage]) -> None:
    for image in images:
        filepath = join(settings.PROJECT_DIR, settings.STATIC_PATH, "sense_images", image.img)
        os.remove(filepath)
        await session.delete(image)


async def add_images_to_sense(
    session: AsyncSession, sense: Sense, image_file_names: Sequence[str]
) -> None:
    for image_file_name in image_file_names:
        db_sense_image = SenseImage(img=image_file_name, sense_id=sense.id, is_public=False)
        session.add(db_sense_image)
    await session.commit()
    await session.refresh(sense)


async def update_definition_part_of_sense_examples(
    session: AsyncSession,
    sense: Sense,
    new_fields: SRequestUpdatePersonalSense,
):
    if new_fields.definition:
        sense.definition = new_fields.definition
    if new_fields.part_of_speech:
        sense.part_of_speech = new_fields.part_of_speech
    if new_fields.examples:
        sense.examples = [Example(example=example) for example in new_fields.examples]
        sense.html_examples = [HtmlExample(html_example=exm) for exm in new_fields.examples]
    await session.commit()
    await session.refresh(sense)


async def delete_personalize_sense(session: AsyncSession, db_sense_with_images: Sense):
    if db_sense_with_images.is_public:
        raise TypeError("received db_sense is not personalize")
    await delete_sense_images(session, db_sense_with_images.sense_images)

    await session.delete(db_sense_with_images)
    await session.commit()
