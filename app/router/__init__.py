from fastapi import APIRouter

from config.config import settings
from .movie import router as movies_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(movies_router)
