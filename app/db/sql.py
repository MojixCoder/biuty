import databases
import sqlalchemy
import ormar

from app.core.settings import get_settings


print(get_settings().DATABASE_URL)


metadata = sqlalchemy.MetaData()
database = databases.Database(get_settings().DATABASE_URL)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
