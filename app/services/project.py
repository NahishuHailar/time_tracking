from typing import Optional

from db.repositories.project import ProjectRepository, get_project_repository
from fastapi import Depends
from schemas.project import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def get_project(self, project_id: int) -> Optional[ProjectSchema]:
        return await self.project_repository.get_by_id(project_id)

    async def create_project(self, project_data: ProjectCreateSchema) -> ProjectSchema:
        return await self.project_repository.create(project_data)

    async def update_project(
        self, project_id: int, project_data: ProjectUpdateSchema
    ) -> ProjectSchema:
        return await self.project_repository.update(project_id, project_data)

    async def delete_project(self, project_id: int) -> None:
        return await self.project_repository.delete(project_id)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(repository)
