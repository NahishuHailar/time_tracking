from typing import Annotated, List

from db.repositories.project_user import (
    ProjectUserRepository,
    get_project_users_repository,
)
from fastapi import Depends
from schemas.project_user import ProjectUserCreateSchema, ProjectUserSchema


class ProjectUserService:
    def __init__(self, project_user_repository: ProjectUserRepository):
        self.project_user_repository = project_user_repository

    async def add_user_to_project(
        self, project_user: ProjectUserCreateSchema
    ) -> ProjectUserSchema:
        return await self.project_user_repository.add_user_to_project(project_user)

    async def remove_user(self, user_id: int, project_id: int) -> None:
        return await self.project_user_repository.remove_user_from_project(
            user_id, project_id
        )

    async def list_project_users(self, project_id: int) -> List[ProjectUserSchema]:
        return await self.project_user_repository.get_project_users(project_id)


def get_project_users_service(
    repository: Annotated[ProjectUserRepository, Depends(get_project_users_repository)],
) -> ProjectUserService:
    return ProjectUserService(repository)
