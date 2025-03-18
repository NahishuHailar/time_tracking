from typing import Optional, Tuple

from redis.asyncio import Redis


class RedisBackend:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        ttl = await self.redis.ttl(key)
        value = await self.redis.get(key)
        return ttl, value

    async def get(self, key: str) -> Optional[bytes]:
        return await self.redis.get(key)

    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        await self.redis.set(key, value, ex=expire)

    async def clear(
            self, namespace: Optional[str] = None,
            key: Optional[str] = None
        ) -> int:
        if namespace:
            keys = await self.redis.keys(f"{namespace}:*")
            if keys:
                await self.redis.delete(*keys)
            return len(keys)
        elif key:
            await self.redis.delete(key)
            return 1
        return 0
