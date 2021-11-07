from enum import IntEnum
from datetime import datetime

import ormar

from app.db.sql import BaseMeta
from app.models.core import City


class Role(IntEnum):
    admin = 1
    store = 2
    user = 3


class User(ormar.Model):
    """
    User model
    """

    id: int = ormar.BigInteger(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True, index=True)
    password: str = ormar.String(max_length=255)
    phone_number: str = ormar.String(max_length=15, unique=True)
    name: str = ormar.String(max_length=100)
    role: Role = ormar.SmallInteger(choices=Role)
    is_active: bool = ormar.Boolean(default=True)
    store_count: int = ormar.SmallInteger(default=0)
    date_joined: datetime = ormar.DateTime(default=datetime.utcnow)

    class Meta(BaseMeta):
        tablename = "users"


class Store(ormar.Model):
    """
    Store model
    """

    id: int = ormar.BigInteger(primary_key=True)
    user: User = ormar.ForeignKey(
        User, nullable=False, ondelete="CASCADE", related_name="store"
    )
    city: City = ormar.ForeignKey(
        City, nullable=False, related_name="stores", ondelete="CASCADE"
    )
    name: str = ormar.String(max_length=100)
    card_number: str = ormar.String(max_length=16)
    address: str = ormar.Text()
    contact_number: str = ormar.String(max_length=20)
    instagram: str = ormar.String(max_length=30, default="")
    telegram: str = ormar.String(max_length=30, default="")

    class Meta(BaseMeta):
        tablename = "stores"
