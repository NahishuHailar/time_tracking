from functools import wraps
from typing import Awaitable, Callable, Optional, TypeVar

from app.cache.cache import FastAPICache
from app.cache.coder import JsonCoder

R = TypeVar("R")

def cache(
    expire: Optional[int] = None,
) -> Callable[[Callable[..., Awaitable[R]]], Callable[..., Awaitable[R]]]:
    """Декоратор для кэширования результатов функции."""

    def wrapper(func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        @wraps(func)
        async def inner(*args, **kwargs) -> R:
            backend = FastAPICache.get_backend()
            prefix = FastAPICache.get_prefix()
            coder = JsonCoder()
            expire_ = expire or FastAPICache.get_expire()

            filtered_kwargs = {
                key: value
                for key, value in kwargs.items()
                if not hasattr(value, "__dict__")
            }

            cache_key = (
            f"{prefix}:{func.__module__}:{func.__name__}:"
            f"{args}:{filtered_kwargs}"
            )

            ttl, cached = await backend.get_with_ttl(cache_key)
            if cached is not None:
                return coder.decode(cached)

            result = await func(*args, **kwargs)
            import time
            time.sleep(4)

            await backend.set(cache_key, coder.encode(result), expire_)

            return result

        return inner

    return wrapper
