import time
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from core.database import db_helper
from . import crud
from .schemas import SRequestSense, SRequestManySense, SResponseSenses

router = APIRouter(prefix="/public_words", tags=["Public words"])


@router.get("/")
async def get_by_alias(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_full_word(session, query)


@router.post("/get_senses", response_model=SResponseSenses)
async def get_by_alias(
    request_senses: SRequestManySense,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return SResponseSenses(senses=await crud.get_senses_by_ids(session, request_senses))


# @router.get("/sense/{sense_id}")
# async def get_sense_by_id(
#     sense_id: int,
#     images_id: list[int] = Query(default=[]),
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     sense = await crud.get_sense_with_word_and_images_by_sense_id(session, sense_id, images_id)
#     return sense
#
#
# @router.get("/image/{image_id}", response_model=ImageDTO)
# async def get_image_by_id(
#     image_id: int,
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     image = await crud.get_image_by_id(session, image_id)
#     if image:
#         return image
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#
# @router.post(
#     "/get_senses_with_images_by_id",
#     response_model=list[SenseDTO],
# )
# async def get_senses_with_images(
#     senses_with_images: RequestSensesWithImages,
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     start = time.time()
#     senses_id = [sense.sense_id for sense in senses_with_images.senses]
#     images_id = [image_id for sense in senses_with_images.senses for image_id in sense.images_ids]
#     result = await crud.get_many_senses_with_word_and_images_by_sense_id(
#         session, senses_id, images_id
#     )
#     logger.info(
#         f"Time for get senses with images and examples: {time.time() - start:.3f}s",
#         format("{level} {time} {message}"),
#     )
#     return result
