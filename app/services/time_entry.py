from fastapi import Depends
from db.repositories.time_entry import TimeEntryRepository
from schemas.time_entry import TimeEntryCreateSchema, TimeEntrySchema
from typing import List

class TimeEntryService:
    def __init__(self, time_entry_repository: TimeEntryRepository = Depends(TimeEntryRepository)):
        self.time_entry_repository = time_entry_repository

    async def log_time(self, time_entry: TimeEntryCreateSchema) -> TimeEntrySchema:
        return await self.time_entry_repository.log_time(time_entry)

    async def get_time_entries(self, user_id: int)-> List[TimeEntrySchema]:
        return await self.time_entry_repository.get_time_entries(user_id)
