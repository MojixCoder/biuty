import pytest
from async_asgi_testclient import TestClient

from app.tests.v1.utils import (
    random_string,
    get_user_data,
    create_and_login_user,
)


BASE_URL = "/api/v1/users"


def get_url(url: str, base_url: str = BASE_URL) -> str:
    return f"{base_url}{url}"


@pytest.mark.asyncio
async def test_sign_up(client: TestClient):
    valid_user_data = get_user_data()
    invalid_user_data = {
        "username": "asd",
        "phone_number": "0916",
        "name": random_string(),
        "password": "1234",
        "verify_password": "1234",
    }

    url = get_url("/signup")
    valid_response = await client.post(path=url, json=valid_user_data)
    invalid_response = await client.post(path=url, json=invalid_user_data)

    errors_count = len(invalid_response.json()["detail"])

    assert valid_response.status_code == 201
    assert valid_response.json()["username"] == valid_user_data["username"].lower()
    assert valid_response.json()["role"] == 2

    assert invalid_response.status_code == 422
    assert errors_count == 3


@pytest.mark.asyncio
async def test_login(client: TestClient):
    user_data = get_user_data()
    url = get_url("/signup")
    response = await client.post(path=url, json=user_data)

    login_data = {
        "username": user_data["username"],
        "password": user_data["password"],
    }

    login_url = get_url("/login")
    login_response = await client.post(path=login_url, form=login_data)
    login_json = login_response.json()

    assert login_response.status_code == 200
    assert isinstance(login_json["access_token"], str)
    assert isinstance(login_json["refresh_token"], str)
    assert login_json["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client: TestClient):
    user_data = await create_and_login_user(client)

    headers = {"Authorization": f"Bearer {user_data['access_token']}"}

    url = get_url("/me")
    response = await client.get(path=url, headers=headers)
    second_response = await client.get(path=url, headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user_data["user"]["id"]

    assert second_response.status_code == 200
    assert second_response.json()["id"] == user_data["user"]["id"]


@pytest.mark.asyncio
async def test_get_refresh_token(client: TestClient):
    user_data = await create_and_login_user(client)

    data = {
        "refresh_token": user_data["refresh_token"],
    }

    url = get_url("/refresh")
    response = await client.post(path=url, json=data)
    response_json = response.json()

    assert response.status_code == 200
    assert isinstance(response_json["access_token"], str)
    assert response_json["token_type"] == "bearer"
