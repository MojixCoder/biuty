from typing import List

from fastapi import APIRouter, Path

from app.core.settings import get_settings
from app.models.core import Province, City
from app.schemas.core import ProvinceSchema, CitySchema


settings = get_settings()
router = APIRouter(prefix="/core", tags=["core"])


@router.get("/province", response_model=List[ProvinceSchema], status_code=200)
async def get_provinces():
    provinces = await Province.objects.all()
    return provinces


@router.get(
    "/province/{province_id}/cities",
    response_model=List[CitySchema],
    response_model_exclude={"province__cities"},
    status_code=200,
    responses={
        404: {
            "content": {
                "application/json": {
                    "example": {"detail": "Not found."},
                }
            },
            "description": "Province with given `province_id` is not found.",
        },
    },
)
async def get_province_cities(province_id: int = Path(..., gt=0)):
    province_exists = await Province.objects.filter(id=province_id).exists()
    if not province_exists:
        raise settings.NOT_FOUND
    cities = (
        await City.objects.filter(province=province_id).select_related("province").all()
    )
    return cities
