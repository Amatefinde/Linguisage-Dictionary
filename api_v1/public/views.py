from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from . import crud

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/")
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_full_word(session, query)
