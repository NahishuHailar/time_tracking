from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import PostgresSettings


class Database:
    def __init__(self, **kwargs):
        settings = PostgresSettings.get_settings(**kwargs)
        self.engine = create_async_engine(settings.url, echo=True)
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
