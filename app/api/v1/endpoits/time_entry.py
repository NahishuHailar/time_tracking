from typing import Annotated, List

from fastapi import APIRouter, Depends
from schemas.time_entry import TimeEntryCreateSchema, TimeEntrySchema
from services.time_entry import TimeEntryService, get_time_entry_service

router = APIRouter()


@router.post("/log_time", response_model=TimeEntrySchema)
async def log_time(
    time_entry: TimeEntryCreateSchema,
    time_entry_service: Annotated[TimeEntryService, Depends(get_time_entry_service)],
):
    return await time_entry_service.log_time(time_entry)


@router.get("/time_entries/{user_id}", response_model=List[TimeEntrySchema])
async def get_time_entries(
    user_id: int,
    time_entry_service: Annotated[TimeEntryService, Depends(get_time_entry_service)],
):
    return await time_entry_service.get_time_entries(user_id)
