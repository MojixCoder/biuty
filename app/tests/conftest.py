import asyncio

import pytest
import sqlalchemy
from async_asgi_testclient import TestClient

from app.main import app
from app.db.sql import metadata, test_database
from app.core.settings import settings


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    engine = sqlalchemy.create_engine(settings.TEST_DATABASE_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture()
async def client():
    async with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module", autouse=True)
async def connect_to_test_database():
    await test_database.connect()
    yield
    await test_database.disconnect()
