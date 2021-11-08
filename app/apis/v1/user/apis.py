from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import get_settings
from app.core.exceptions import CONFLICT, BAD_REQUEST, UNAUTHORIZED, PERMISSION_DENIED
from app.core.passwords import hash_password, verify_password
from app.core.jwt import jwt_manager
from app.models.user import User, Role
from app.permissions.user import get_current_active_user
from app.schemas.user import UserSchema, SignUpSchema, TokenSchema, RefreshSchema


settings = get_settings()
router = APIRouter(prefix="/users", tags=["user"])


@router.post(
    "/signup",
    response_model=UserSchema,
    status_code=201,
    responses={
        CONFLICT.status_code: {
            "content": {
                "application/json": {
                    "example": {"detail": CONFLICT.detail},
                }
            },
            "description": "A user with given `username` already exists.",
        },
    },
)
async def sign_up(user_data: SignUpSchema):
    user_exists = await User.objects.filter(username=user_data.username).exists()
    if user_exists:
        raise CONFLICT
    user_data = user_data.dict()
    password = user_data.pop("verify_password")
    user_data["password"] = hash_password(password)
    user = await User.objects.create(**user_data, role=Role.user)
    return user


@router.post(
    "/login",
    response_model=TokenSchema,
    status_code=200,
    responses={
        BAD_REQUEST.status_code: {
            "content": {
                "application/json": {
                    "example": {"detail": BAD_REQUEST.detail},
                }
            },
            "description": "User not found or incorrect password.",
        }
    },
)
async def login(login_data: OAuth2PasswordRequestForm = Depends()):
    username = login_data.username.lower()
    user = await User.objects.get_or_none(username=username)
    if user is None:
        raise BAD_REQUEST
    is_correct_password = verify_password(
        plain_password=login_data.password, hashed_password=user.password
    )
    if is_correct_password is False:
        raise BAD_REQUEST
    tokens = jwt_manager.user_login_response(str(user.id))
    return tokens


@router.post(
    "/refresh",
    response_model=RefreshSchema,
    status_code=200,
    responses={
        BAD_REQUEST.status_code: {
            "content": {
                "application/json": {
                    "example": {"detail": BAD_REQUEST.detail},
                }
            },
            "description": "Invalid refresh token.",
        }
    },
)
async def refresh(refresh_token: str = Body(..., embed=True)):
    tokens = jwt_manager.create_token_from_refresh(refresh_token)
    return tokens


@router.get(
    "/me",
    response_model=UserSchema,
    status_code=200,
    responses={
        UNAUTHORIZED.status_code: {
            "content": {
                "application/json": {
                    "example": {"detail": UNAUTHORIZED.detail},
                }
            },
            "description": "User is not authorized.",
        },
        PERMISSION_DENIED.status_code: {
            "content": {
                "application/json": {
                    "example": {"detail": PERMISSION_DENIED.detail},
                }
            },
            "description": "User is not active",
        },
    },
)
async def me(user: User = Depends(get_current_active_user)):
    return dict(user)
