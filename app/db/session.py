from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.db_url, echo=True)
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

database = Database()
