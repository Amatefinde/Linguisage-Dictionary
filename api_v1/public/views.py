from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from . import crud
from .schemas import SResponse
from background_tasks.tasks import find_and_add_world


router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/", response_model=SResponse)
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response: SResponse = await crud.get_full_word(session, query)
    if not response:
        find_and_add_world.delay(query)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return response
