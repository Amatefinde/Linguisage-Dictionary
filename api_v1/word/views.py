from fastapi import APIRouter, Depends, HTTPException, status
from core.database import db_helper
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/words", tags=["Words"])


@router.get("/find_word_and_save_to_db")
async def find_word_and_save_to_db(
    word: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return


@router.get("/alias")
async def get_by_alias(
    alias: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    word_dto = await crud.get_all_word_data(session, alias)
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
