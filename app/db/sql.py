import databases
import sqlalchemy
import ormar

from app.core.settings import settings


metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)
test_database = databases.Database(settings.TEST_DATABASE_URL)


if settings.TEST:
    class BaseMeta(ormar.ModelMeta):
        metadata = metadata
        database = test_database
else:
    class BaseMeta(ormar.ModelMeta):
        metadata = metadata
        database = database
