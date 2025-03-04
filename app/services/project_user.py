from fastapi import Depends
from db.repositories.project_user import ProjectUserRepository
from schemas.project_user import ProjectUserCreateSchema, ProjectUserSchema
from typing import List


class ProjectUserService:
    def __init__(
        self,
        project_user_repository: ProjectUserRepository = Depends(ProjectUserRepository),
    ):
        self.project_user_repository = project_user_repository

    async def add_user_to_project(self, project_user: ProjectUserCreateSchema) -> ProjectUserSchema:
        return await self.project_user_repository.add_user_to_project(project_user)

    async def remove_user(self, user_id: int, project_id: int) -> None:
        return await self.project_user_repository.remove_user_from_project(
            user_id, project_id
        )

    async def list_project_users(self, project_id: int) -> List[ProjectUserSchema]:
        return await self.project_user_repository.get_project_users(project_id)
