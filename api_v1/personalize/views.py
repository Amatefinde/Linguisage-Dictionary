from os.path import join
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from .depends import get_personalize_sense_with_all_field
from core.database.models import Sense
from . import crud
from core import settings
from core.database import db_helper
from .schemas import SRequestAddPersonalizeSense, SPersonalizeSense, SRequestUpdatePersonalSense
from utils.image_processing import base64_strings_to_images, save_images

router = APIRouter(tags=["Personalize"], prefix="/personalize")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_custom_sense(
    add_sense_request: SRequestAddPersonalizeSense,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    images: list[Image] = base64_strings_to_images(add_sense_request.images_base64str)
    path_to_images_dir = str(join(settings.PROJECT_DIR, settings.STATIC_PATH, "sense_images"))
    filenames: list[str] = save_images(path_to_images_dir, images)
    personalize_sense = SPersonalizeSense.model_validate(add_sense_request, from_attributes=True)
    personalize_sense.image_filenames = filenames
    db_sense = await crud.add_sense(session, personalize_sense)
    return db_sense


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personalize_sense(
    db_sense_personalize_with_images: Annotated[
        Sense, Depends(get_personalize_sense_with_all_field)
    ],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_personalize_sense(session, db_sense_personalize_with_images)


@router.patch("/", status_code=status.HTTP_200_OK)
async def delete_personalize_sense(
    db_sense_personalize_with_images: Annotated[
        Sense, Depends(get_personalize_sense_with_all_field)
    ],
    request_update_sense: SRequestUpdatePersonalSense,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if request_update_sense.images_base64str:
        await crud.delete_sense_images(session, db_sense_personalize_with_images.sense_images)
        images: list[Image] = base64_strings_to_images(request_update_sense.images_base64str)
        path_to_images_dir = str(join(settings.PROJECT_DIR, settings.STATIC_PATH, "sense_images"))
        filenames: list[str] = save_images(path_to_images_dir, images)
        await crud.add_images_to_sense(session, db_sense_personalize_with_images, filenames)

    await crud.update_definition_part_of_sense_examples(
        session,
        db_sense_personalize_with_images,
        request_update_sense,
    )
