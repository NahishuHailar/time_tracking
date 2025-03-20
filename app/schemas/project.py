from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectBaseSchema(BaseModel):
    name: str


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: int

    class Config:
        from_attributes = True
