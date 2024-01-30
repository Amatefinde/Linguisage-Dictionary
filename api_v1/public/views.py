from typing import Literal, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from loguru import logger
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from . import crud
from .schemas import SResponse
from background_tasks.tasks import find_and_add_world


router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/query", response_model=SResponse)
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response: SResponse = await crud.get_full_word(session, query)
    if not response:
        find_and_add_world.delay(query)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return response


@router.get("/random")
async def get_random(
    amount: Annotated[int, Query(ge=1, le=100)],
    lvl: Annotated[list[Literal["A1", "A2", "B1", "B2", "C1", "C2"]], Query()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_random_words(session, amount, lvl)
