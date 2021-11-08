import databases
import sqlalchemy
import ormar

from app.core.settings import get_settings


metadata = sqlalchemy.MetaData()
database = databases.Database(get_settings().DATABASE_URL)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
