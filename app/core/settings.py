import os
from functools import lru_cache
from datetime import timedelta

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings
    """

    # Application settings
    DEBUG: bool = os.getenv("DEBUG")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_DB: int = os.getenv("REDIS_DB")

    # URL settings
    API_STR: str = "/api"
    V1_STR: str = "/v1"

    # JWT settings
    JWT_ALGORITHM = "HS512"
    JWT_REFRESH_EXPIRE_TIME: timedelta = timedelta(days=365)
    JWT_ACCESS_EXPIRE_TIME: timedelta = timedelta(days=1)

    # Regex
    USERNAME_REGEX: str = "(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])"
    PASSWORD_REGEX: str = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$"
    PHONE_NUMBER_REGEX: str = "^[0][9][0-9]{9}$"
    INSTAGRAM_REGEX: str = (
        "([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
    )

    # Cache keys
    USER_CACHE_KEY: str = "users"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
