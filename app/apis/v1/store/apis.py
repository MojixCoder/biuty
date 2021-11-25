from typing import Dict, Any

from fastapi import APIRouter, Depends, Body
from fastapi_pagination import Page, Params, paginate

from app.permissions.user import get_current_active_user, admin_user
from app.core.exceptions import BAD_REQUEST
from app.models.core import City
from app.models.store import Store, StoreBarbers
from app.schemas.store import StoreSchema, StoreCreateSchema, StoreCreateResponseSchema

router = APIRouter(prefix="/store", tags=["store"])


@router.get("", response_model=Page[StoreSchema])
async def get_stores(
    params: Params = Depends(), user: Dict[str, Any] = Depends(admin_user)
):
    stores = await Store.objects.select_related(
        ["user", "city", "city__province"]
    ).all()
    return paginate(stores, params)


@router.post("", response_model=StoreCreateResponseSchema, status_code=201)
async def create_store(
    store_data: StoreCreateSchema,
    user: Dict[str, Any] = Depends(get_current_active_user),
):
    city_exists = await City.objects.filter(id=store_data.city).exists()
    if not city_exists:
        raise BAD_REQUEST
    store = await Store.objects.create(**store_data.dict(), user=user["id"])
    store_response = store.dict()
    store_response["city"] = store.city.id
    store_response["user"] = store.user.id
    return store_response
