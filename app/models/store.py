from datetime import datetime, date

import ormar

from app.db.sql import BaseMeta
from app.models.user import User
from app.models.core import City


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
    is_active: bool = ormar.Boolean(default=False)
    card_number: str = ormar.String(max_length=16)
    address: str = ormar.Text()
    contact_number: str = ormar.String(max_length=20)
    instagram: str = ormar.String(max_length=30, default="")
    telegram: str = ormar.String(max_length=30, default="")
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)

    class Meta(BaseMeta):
        tablename = "stores"


class StoreBarbers(ormar.Model):
    """
    Store barbers model
    """

    id: int = ormar.BigInteger(primary_key=True)
    user: User = ormar.ForeignKey(
        User, nullable=False, ondelete="CASCADE", related_name="store_barbers"
    )
    store: Store = ormar.ForeignKey(
        Store, nullable=False, ondelete="CASCADE", related_name="store_barbers"
    )
    is_active: bool = ormar.Boolean(default=True)
    joined_at: date = ormar.Date(default=datetime.utcnow)
    left_at: date = ormar.Date(nullable=True)

    class Meta(BaseMeta):
        tablename = "store_x_user"
