from pydantic import BaseModel


class ProjectUserBaseSchema(BaseModel):
    project_id: int
    user_id: int
    role: str = "employee"


class ProjectUserCreateSchema(ProjectUserBaseSchema):
    pass


class ProjectUserSchema(ProjectUserBaseSchema):
    id: int

    class Config:
        from_attributes = True
