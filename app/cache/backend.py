from typing import Optional, Tuple

from redis.asyncio import Redis

from app.db.session import get_redis_db


class RedisClient:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        ttl = await self._redis.ttl(key)
        value = await self._redis.get(key)
        return ttl, value

    async def get(self, key: str) -> Optional[bytes]:
        return await self._redis.get(key)

    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        await self._redis.set(key, value, ex=expire)

    async def clear(
        self, namespace: Optional[str] = None, key: Optional[str] = None
    ) -> int:
        if namespace:
            keys = await self._redis.keys(f"{namespace}:*")
            if keys:
                await self._redis.delete(*keys)
            return len(keys)
        elif key:
            await self._redis.delete(key)
            return 1
        return 0


async def get_redis_client():
    redis_db = get_redis_db()
    client = await redis_db.get_client()
    return RedisClient(client)
