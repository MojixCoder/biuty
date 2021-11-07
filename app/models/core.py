import ormar

from app.db.sql import BaseMeta


class Province(ormar.Model):
    """
    Province model
    """

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)

    class Meta(BaseMeta):
        tablename = "provinces"


class City(ormar.Model):
    """
    City model
    """

    id: int = ormar.Integer(primary_key=True)
    province: Province = ormar.ForeignKey(
        Province, nullable=False, related_name="cities", ondelete="CASCADE"
    )
    name: str = ormar.String(max_length=50)

    class Meta(BaseMeta):
        tablename = "cities"
