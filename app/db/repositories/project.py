from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import ProjectORM
from app.db.session import get_database
from app.exceptions import NotFoundError
from app.schemas.project import ProjectCreateSchema, ProjectUpdateSchema


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: int) -> Optional[ProjectORM]:
        project = await self.db.get(ProjectORM, project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project

    async def create(self, project_data: ProjectCreateSchema) -> ProjectORM:
        project = ProjectORM(**project_data.model_dump())
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def update(
        self, project_id: int, project_data: ProjectUpdateSchema
    ) -> ProjectORM:
        project = await self.get_by_id(project_id)
        for key, value in project_data.model_dump().items():
            setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project_id: int) -> None:
        project = await self.get_by_id(project_id)
        await self.db.delete(project)
        await self.db.flush()


def get_project_repository(
    db: Annotated[AsyncSession, Depends(get_database().get_db)],
) -> ProjectRepository:
    return ProjectRepository(db)
