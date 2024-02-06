from typing import Literal, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from loguru import logger
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from core.types import level_type, main_pos_type, main_pos
from . import crud
from .schemas import SWordResponse, SRandomSensesResponse, SPickedRandomSense, SAdditionalPOSs
from background_tasks.tasks import find_and_add_world


router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/query", response_model=SWordResponse)
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    query = query.lower()
    response: SWordResponse = await crud.get_full_word(session, query)
    if not response:
        find_and_add_world.delay(query)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return response


@router.get("/random", response_model=SRandomSensesResponse)
async def get_random(
    amount: Annotated[int, Query(ge=1, le=100)],
    lvl: Annotated[list[level_type], Query()] = None,
    pos: Annotated[list[main_pos_type], Query()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not pos:
        pos = main_pos
    picked_senses: list[SPickedRandomSense] = await crud.get_random_senses(
        session, amount, lvl, pos, load_examples_and_images=True
    )
    picked_part_of_speeches = {sense.part_of_speech for sense in picked_senses}
    picked_senses_ids = [sense.id for sense in picked_senses]
    additional_part_of_speeches = SAdditionalPOSs()
    for part_of_speech in picked_part_of_speeches:
        additional_senses = await crud.get_random_senses(
            session,
            amount if amount > 15 else amount * 3,
            lvl,
            [part_of_speech],
            picked_senses_ids,
        )
        setattr(additional_part_of_speeches, part_of_speech, additional_senses)

    return SRandomSensesResponse(senses=picked_senses, additional=additional_part_of_speeches)
