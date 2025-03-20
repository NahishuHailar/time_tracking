import json
from functools import wraps
from typing import Awaitable, Callable, Optional, TypeVar

from pydantic import BaseModel

from app.cache.backend import get_redis_client
from app.schemas.project import ProjectSchema

R = TypeVar("R")


def cache(
    expire: Optional[int] = None,
) -> Callable[[Callable[..., Awaitable[R]]], Callable[..., Awaitable[R]]]:
    def wrapper(func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        @wraps(func)
        async def inner(*args, **kwargs) -> R:
            redis = await get_redis_client()
            prefix = "time_tracking"
            expire_ = expire or 5

            filtered_kwargs = {
                key: value
                for key, value in kwargs.items()
                if not hasattr(value, "__dict__")
            }

            cache_key = (
                f"{prefix}:{func.__module__}:{func.__name__}:"
                f"{args}:{filtered_kwargs}"
            )

            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if hasattr(result, "__mapper__"):  # Check if result is a SQLAlchemy object
                result = ProjectSchema.from_orm(result)

            if isinstance(result, BaseModel):
                encode_result = result.model_dump_json()
            else:
                encode_result = json.dumps(result)

            await redis.set(cache_key, encode_result, expire_)

            return result

        return inner

    return wrapper
