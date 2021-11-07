import re
from datetime import datetime

from pydantic import BaseModel, validator, root_validator, Field

from app.models.user import Role
from app.core.settings import get_settings


settings = get_settings()


class UserSchema(BaseModel):
    """
    User model schema
    """

    id: int
    username: str
    phone_number: str
    role: Role
    name: str
    is_active: bool
    store_count: int
    date_joined: datetime

    class Config:
        orm_mode = True


class SignUpSchema(BaseModel):
    """
    User sign up schema
    """

    username: str
    phone_number: str
    name: str = Field(..., min_length=3)
    password: str
    verify_password: str

    @validator("username")
    def validate_username(cls, value):  # noqa
        if not re.match(settings.USERNAME_REGEX, value):
            raise ValueError("Invalid username.")
        return value.lower()

    @validator("phone_number")
    def validate_phone_number(cls, value):  # noqa
        if not re.match(settings.PHONE_NUMBER_REGEX, value):
            raise ValueError("Invalid phone number.")
        return value

    @validator("password")
    def validate_password(cls, value):  # noqa
        if not re.match(settings.PASSWORD_REGEX, value):
            raise ValueError("Invalid password.")
        return value

    @root_validator
    def check_passwords_match(cls, values):  # noqa
        password = values.get("password")
        verify_password = values.get("verify_password")
        if (
            password is not None
            and verify_password is not None
            and password != verify_password
        ):
            raise ValueError("Passwords don't match.")
        return values


class TokenSchema(BaseModel):
    """
    Login schema
    """

    access_token: str
    refresh_token: str
    token_type: str


class RefreshSchema(BaseModel):
    """
    Refresh schema
    """
    access_token: str
    token_type: str
