from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_env_settings


class Database:
    def __init__(self, **kwargs):
        self.engine = create_async_engine(get_env_settings(**kwargs).db_url, echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_db(self):
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
    return Database()
