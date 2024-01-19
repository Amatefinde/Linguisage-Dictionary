from fastapi import APIRouter

# from .word import word_router

__all__ = ["router"]

router = APIRouter(prefix="/api/v1")
# router.include_router(word_router)
