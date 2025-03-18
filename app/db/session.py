from abc import ABC, abstractmethod
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import BaseSettingsConfig, PostgresSettings


class BaseDatabase(ABC):
    def __init__(self, settings: BaseSettingsConfig):
        self.settings = settings

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def get_client(self):
        pass



class PostgresDatabase(BaseDatabase):
    def __init__(self, **kwargs):
        settings = PostgresSettings.get_settings(**kwargs)
        super().__init__(settings)
        self.engine = create_async_engine(self.settings.url, echo=self.settings.pg_echo)
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


