from pydantic import BaseModel
from datetime import date

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    time_entries: list["TimeEntry"] = []

    class Config:
        from_attributes = True