from fastapi import APIRouter

from app.core.settings import get_settings
from app.apis.v1.router import v1_router

router = APIRouter(prefix=get_settings().API_STR)

router.include_router(v1_router)
