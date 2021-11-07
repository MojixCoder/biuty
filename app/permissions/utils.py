from app.core.jwt import jwt_manager
from app.core.settings import get_settings
from app.core.exceptions import UNAUTHORIZED
from app.db.redis import redis, load_val, dump_val
from app.models.user import User


def get_token_from_header(token: str) -> str:
    prefix = "Bearer "
    if not token.startswith(prefix):
        raise jwt_manager.credentials_exception
    skipped_chars = len(prefix)
    return token[skipped_chars:]


async def get_or_set_user_in_cache(user_id: int) -> User:
    user_cache_key_prefix = get_settings().USER_CACHE_KEY
    user_cache_key = f"{user_cache_key_prefix}_{user_id}"
    user = await redis.get(user_cache_key)
    if user is not None:
        user = load_val(user)
        return user
    user = await User.objects.get_or_none(id=user_id)
    if user is None:
        raise UNAUTHORIZED
    dumped_user = dump_val(user)
    await redis.set(name=user_cache_key, value=dumped_user, ex=86400)
    return user
