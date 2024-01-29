from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from . import crud
from .schemas import SResponse

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/", response_model=SResponse)
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_full_word(session, query)
