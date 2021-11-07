from fastapi import Depends, Header

from app.core.exceptions import UNAUTHORIZED, PERMISSION_DENIED
from app.core.jwt import jwt_manager
from app.models.user import User
from app.permissions.utils import get_token_from_header, get_or_set_user_in_cache


async def get_current_user(authorization: str = Header(...)) -> User:
    """
    Current user
    """
    try:
        token = get_token_from_header(authorization)
        payload = jwt_manager.decode_token(token)
        if payload["token_type"] != "access":
            raise UNAUTHORIZED
        user_id: int = payload[jwt_manager.user_id_claim]
        user = await get_or_set_user_in_cache(user_id)
        return user
    except:
        raise UNAUTHORIZED


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Current active user
    """
    if not current_user.is_active:
        raise PERMISSION_DENIED
    return current_user
