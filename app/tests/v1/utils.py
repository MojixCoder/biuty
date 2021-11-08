import random
import string
from typing import Dict, Any

from async_asgi_testclient import TestClient


def random_string(k: int = 8) -> str:
    return "".join(random.choices(string.ascii_letters, k=k))


def random_password(k: int = 8) -> str:
    random_str = random_string(k)
    password = f"Ab1234{random_str}"
    return password


def random_email() -> str:
    random_str = random_string().lower()
    return f"{random_str}@{random_str[:4]}.com"


def random_phone_number() -> str:
    number = "".join(random.choices(string.digits, k=9))
    return f"09{number}"


def get_user_data() -> Dict[str, Any]:
    password = random_password()
    data = {
        "username": random_string(),
        "phone_number": random_phone_number(),
        "name": random_string(),
        "password": password,
        "verify_password": password,
    }
    return data


async def create_and_login_user(client: TestClient) -> Dict[str, Any]:
    user_data = get_user_data()
    url = "/api/v1/users/signup"
    response = await client.post(path=url, json=user_data)
    user_json = response.json()

    login_data = {
        "username": user_data["username"],
        "password": user_data["password"],
    }

    login_url = "/api/v1/users/login"
    login_response = await client.post(path=login_url, form=login_data)
    login_json = login_response.json()

    data = {
        "user": user_json,
        **login_json,
    }

    return data
