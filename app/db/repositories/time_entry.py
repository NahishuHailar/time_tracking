from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.time_entry import TimeEntryORM
from db.session import database
from schemas.time_entry import TimeEntryCreateSchema
from typing import List


class TimeEntryRepository:
    def __init__(self, db: AsyncSession = Depends(database.get_db)):
        self.db = db

    async def log_time(self, time_entry: TimeEntryCreateSchema) -> TimeEntryORM:
        new_entry = TimeEntryORM(**time_entry.model_dump())
        self.db.add(new_entry)
        await self.db.flush()  
        return new_entry

    async def get_time_entries(self, user_id: int)-> List[TimeEntryORM]:
        query = select(TimeEntryORM).where(TimeEntryORM.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
