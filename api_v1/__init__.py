from fastapi import APIRouter

from .public import router as public_router
from .personalize import router as personalize_router
from .common import router as common_router

__all__ = ["router"]

router = APIRouter(prefix="/api/v1")
router.include_router(common_router)
router.include_router(public_router)
router.include_router(personalize_router)
