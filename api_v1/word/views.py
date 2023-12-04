from fastapi import APIRouter, Depends, HTTPException, status, Query
from core.database import db_helper
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from Parsers.word_collector import search_by_query_and_save_to_db, get_word_by_alias
from .schemas import WordDTO, ImageDTO

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
