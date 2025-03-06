from typing import List

from db.repositories.time_entry import TimeEntryRepository, get_time_entry_repository
from fastapi import Depends
from schemas.time_entry import TimeEntryCreateSchema, TimeEntrySchema


class TimeEntryService:
    def __init__(self, time_entry_repository: TimeEntryRepository):
        self.time_entry_repository = time_entry_repository

    async def log_time(self, time_entry: TimeEntryCreateSchema) -> TimeEntrySchema:
        return await self.time_entry_repository.log_time(time_entry)

    async def get_time_entries(self, user_id: int) -> List[TimeEntrySchema]:
        return await self.time_entry_repository.get_time_entries(user_id)


def get_time_entry_service(
    repository: TimeEntryRepository = Depends(get_time_entry_repository),
) -> TimeEntryService:
    return TimeEntryService(repository)
