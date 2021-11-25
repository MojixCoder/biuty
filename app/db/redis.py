import pickle
from typing import Any

import aioredis

from app.core.settings import settings


redis = aioredis.from_url(
    url=settings.REDIS_HOST,
    db=settings.REDIS_DB,
)


def dump_val(value: Any) -> bytes:
    pickled_value = pickle.dumps(value)
    return pickled_value


def load_val(value: bytes) -> Any:
    python_value = pickle.loads(value)
    return python_value
