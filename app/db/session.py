from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL, echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_db(self):
        async with self.async_session() as session:
            yield session

database = Database()