from loguru import logger
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.models import Word, SenseImage, Example, Sense, Alias, WordImage
from core.schemas.schemas import CoreSWord, CoreSSense
from utils import async_timer
from .schemas import SRequestSense, SRequestManySenseWithContent, SResponseSense, SImage


@async_timer
async def get_senses_by_ids(session: AsyncSession, request_senses: SRequestManySenseWithContent):
    word_image_ids = []
    sense_image_ids = []
    senses_map: dict[int, SRequestSense] = {}
    for request_sense in request_senses.senses:
        senses_map[request_sense.sense_id] = request_sense
        word_image_ids.extend(request_sense.word_image_ids)
        sense_image_ids.extend(request_sense.sense_image_ids)

    stmt = (
        select(Sense)
        .options(
            joinedload(Sense.examples),
            joinedload(Sense.word),
            selectinload(Sense.word, Word.word_images.and_(WordImage.id.in_(word_image_ids))),
            selectinload(Sense.sense_images.and_(SenseImage.id.in_(sense_image_ids))),
        )
        .join(Word, Sense.word_id == Word.id)
        .join(WordImage, WordImage.word_id == Word.id, isouter=True)
        .join(SenseImage, SenseImage.sense_id == Sense.id, isouter=True)
        .where(Sense.id.in_(senses_map))
    )
    row_response = await session.execute(stmt)

    senses_for_response = []
    for sense in row_response.unique().mappings().all():
        ready_sense = SResponseSense.model_validate(sense["Sense"], from_attributes=True)
        ready_sense.word_images = [
            SImage.model_validate(image, from_attributes=True)
            for image in sense.Sense.word.word_images
            if image.id in senses_map[sense.Sense.id].word_image_ids  # keep only requested img
        ]
        senses_for_response.append(ready_sense)
    return senses_for_response
