from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserForeignKeySchema
from app.schemas.core import CitySchema


class StoreSchema(BaseModel):
    """
    Store schema
    """

    id: int
    user: UserForeignKeySchema
    city: CitySchema
    name: str
    is_active: bool
    card_number: str
    address: str
    contact_number: str
    instagram: str
    telegram: str
    created_at: datetime

    class Config:
        orm_mode = True


class StoreCreateSchema(BaseModel):
    """
    Store create schema
    """

    city: int = Field(..., gt=0)
    name: str
    card_number: str
    address: str
    contact_number: str
    instagram: str = ""
    telegram: str = ""


class StoreCreateResponseSchema(BaseModel):
    """
    Store create response schema
    """

    id: int
    user: int
    city: int
    name: str
    is_active: bool
    card_number: str
    address: str
    contact_number: str
    instagram: str
    telegram: str
    created_at: datetime

    class Config:
        orm_mode = True
