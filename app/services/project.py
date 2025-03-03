from app.db.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, Project

class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def get_project(self, project_id: int) -> Project:
        return await self.project_repository.get_by_id(project_id)

    async def create_project(self, project_data: ProjectCreate) -> Project:
        return await self.project_repository.create(project_data)

    async def update_project(self, project_id: int, project_data: ProjectUpdate) -> Project:
        return await self.project_repository.update(project_id, project_data)

    async def delete_project(self, project_id: int) -> bool:
        return await self.project_repository.delete(project_id)