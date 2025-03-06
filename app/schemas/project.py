from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectBaseSchema(BaseModel):
    name: str
    # description: Optional[str] = None


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: int
    # owner_id: int
    # created_at: datetime

    class Config:
        from_attributes = True
