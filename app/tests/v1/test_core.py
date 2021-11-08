import pytest
from async_asgi_testclient import TestClient

from app.db.sql import test_database
from app.models.core import Province, City
from app.tests.v1.utils import random_string


BASE_URL = "/api/v1/core"


def get_url(url: str, base_url: str = BASE_URL) -> str:
    return f"{base_url}{url}"


@pytest.mark.asyncio
async def test_get_provinces(client: TestClient):
    Province.Meta.database = test_database

    province = await Province.objects.create(name=random_string())

    url = get_url("/province")
    response = await client.get(path=url)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert response_json[0]["id"] == province.id


@pytest.mark.asyncio
async def test_get_province_cities(client: TestClient):
    Province.Meta.database = test_database
    City.Meta.database = test_database

    province1 = await Province.objects.create(name=random_string())
    province2 = await Province.objects.create(name=random_string())

    city1 = await City.objects.create(province=province1, name=random_string())
    city2 = await City.objects.create(province=province1, name=random_string())
    city3 = await City.objects.create(province=province2, name=random_string())

    url = get_url(f"/province/{province1.id}/cities")
    response = await client.get(path=url)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 2

    for city in response_json:
        assert city["province"]["id"] == province1.id
