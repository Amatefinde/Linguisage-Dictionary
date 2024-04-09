from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import SRequestManySenseWithContent, SResponseSenses
from core.database import db_helper

router = APIRouter(prefix="/general", tags=["General"])


@router.post("/get_senses", response_model=SResponseSenses)
async def get_senses_with_images(
    request_senses: SRequestManySenseWithContent,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return SResponseSenses(senses=await crud.get_senses_by_ids(session, request_senses))
