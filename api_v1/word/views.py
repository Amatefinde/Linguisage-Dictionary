import asyncio
import time

from fastapi import APIRouter, Depends, HTTPException, status, Query
from loguru import logger

from core.database import db_helper
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from Parsers.word_collector import search_by_query_and_save_to_db, get_word_by_alias
from .schemas import WordDTO, ImageDTO, RequestSensesWithImages, SenseDTO

router = APIRouter(prefix="/words", tags=["Words"])


@router.get("/alias", response_model=WordDTO)
async def get_by_alias(
    alias: str,
    download_if_not_found: bool = True,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_dto = await crud.get_all_word_data(session, alias)
    if word_dto:
        return word_dto
    elif word_dto := await crud.get_all_word_data(session, await get_word_by_alias(alias)):
        await crud.add_alias_to_word(session, alias, word_dto.word)
        return word_dto

    elif download_if_not_found:
        word_dto = await search_by_query_and_save_to_db(session, alias)
        if word_dto:
            return word_dto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/sense/{sense_id}")
async def get_sense_by_id(
    sense_id: int,
    images_id: list[int] = Query(default=[]),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sense = await crud.get_sense_with_word_and_images_by_sense_id(session, sense_id, images_id)
    return sense


@router.get("/image/{image_id}", response_model=ImageDTO)
async def get_image_by_id(
    image_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    image = await crud.get_image_by_id(session, image_id)
    if image:
        return image
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/get_senses_with_images_by_id",
    response_model=list[SenseDTO],
)
async def get_senses_with_images(
    senses_with_images: RequestSensesWithImages,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    tasks = []
    start = time.time()
    senses_id = [sense.sense_id for sense in senses_with_images.senses]
    images_id = [image_id for sense in senses_with_images.senses for image_id in sense.images_ids]
    result = await crud.get_many_senses_with_word_and_images_by_sense_id(
        session, senses_id, images_id
    )
    logger.info(
        f"Time for get senses with images and examples: {time.time() - start:.3f}s",
        format("{level} {time} {message}"),
    )
    return result
