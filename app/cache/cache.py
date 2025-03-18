from typing import Optional

from app.cache.backend import RedisBackend


class FastAPICache:
    _backend: Optional[RedisBackend] = None
    _prefix: str = ""
    _expire: Optional[int] = None

    @classmethod
    def init(
        cls,
        backend: RedisBackend,
        prefix: str = "",
        expire: Optional[int] = None,
    ) -> None:
        cls._backend = backend
        cls._prefix = prefix
        cls._expire = expire

    @classmethod
    def get_backend(cls) -> RedisBackend:
        assert cls._backend, "You must call init first!"
        return cls._backend

    @classmethod
    def get_prefix(cls) -> str:
        return cls._prefix

    @classmethod
    def get_expire(cls) -> Optional[int]:
        return cls._expire
