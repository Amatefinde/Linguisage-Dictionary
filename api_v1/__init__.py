from fastapi import APIRouter

from .public_word import router as public_word_router

__all__ = ["router"]

router = APIRouter(prefix="/api/v1")
router.include_router(public_word_router)
