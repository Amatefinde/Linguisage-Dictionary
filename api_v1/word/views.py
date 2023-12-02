from fastapi import APIRouter, Depends
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


@router.get("/words")
async def get_by_alias(
    alias: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_word_data(session, alias)
