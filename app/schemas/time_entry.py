from pydantic import BaseModel
from datetime import date

class TimeEntryBaseSchema(BaseModel):
    project_id: int
    user_id: int
    hours: float
    date: date


class TimeEntryCreateSchema(TimeEntryBaseSchema):
    pass

class TimeEntrySchema(TimeEntryBaseSchema):
    id: int

    class Config:
        from_attributes = True

        