from functools import lru_cache

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import EnvSettings


class PostgresDatabase:
    def __init__(self, **kwargs):
        settings = EnvSettings.get_settings(**kwargs)
        self.engine = create_async_engine(
            settings.postgres_url, echo=settings.postgres_echo
        )
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def connect(self):
        return self.async_session

    async def disconnect(self):
        await self.engine.dispose()

    async def get_client(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
            finally:
                await session.close()


@lru_cache
def get_database():
    return PostgresDatabase()


class RedisDatabase:
    def __init__(self, **kwargs):
        settings = EnvSettings.get_settings(**kwargs)
        self._client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    async def connect(self):
        try:
            await self._client.ping()
            return self._client
        except redis.ConnectionError as e:
            raise Exception(f"Redis error connection: {e}") from e

    async def disconnect(self):
        await self._client.close()

    async def get_client(self):
        return self._client


@lru_cache
def get_redis_db():
    return RedisDatabase()
