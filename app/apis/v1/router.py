from fastapi import APIRouter

from app.core.settings import settings
from app.apis.v1.user.apis import router as user_router
from app.apis.v1.core.apis import router as core_router
from app.apis.v1.store.apis import router as store_router


v1_router = APIRouter(prefix=settings.V1_STR)

v1_router.include_router(user_router)
v1_router.include_router(core_router)
v1_router.include_router(store_router)
