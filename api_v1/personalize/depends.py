from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from . import crud


async def get_personalize_sense_with_all_field(
    sense_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_sense_with_imgs = await crud.get_db_sense_with_all_field(session, sense_id)
    if not db_sense_with_imgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is not personalize sense with this id",
        )
    if db_sense_with_imgs.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You trying to delete public sense!",
        )
    return db_sense_with_imgs
