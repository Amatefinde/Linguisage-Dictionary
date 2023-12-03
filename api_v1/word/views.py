from fastapi import APIRouter, Depends, HTTPException, status
from core.database import db_helper
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from Parsers.word_collector import search_by_query_and_save_to_db

router = APIRouter(prefix="/words", tags=["Words"])


@router.get("/alias")
async def get_by_alias(
    alias: str,
    download_if_not_found: bool = False,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_dto = await crud.get_all_word_data(session, alias)
    if word_dto:
        return word_dto
    elif download_if_not_found:
        word_dto = await search_by_query_and_save_to_db(session, alias)
        if word_dto:
            return word_dto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/sense/{sense_id}")
async def get_sense_by_id(
    sense_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    sense = await crud.get_sense_with_word_and_images_by_sense_id(session, sense_id)
    return sense
