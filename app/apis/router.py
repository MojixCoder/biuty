from fastapi import APIRouter

from app.core.settings import settings
from app.apis.v1.router import v1_router

router = APIRouter(prefix=settings.API_STR)

router.include_router(v1_router)
