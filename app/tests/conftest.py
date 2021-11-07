import asyncio

import pytest
import sqlalchemy
from async_asgi_testclient import TestClient

from app.main import app
from app.db.sql import metadata
from app.core.settings import get_settings


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    engine = sqlalchemy.create_engine(get_settings().TEST_DATABASE_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture()
async def client():
    async with TestClient(app) as client:
        yield client
