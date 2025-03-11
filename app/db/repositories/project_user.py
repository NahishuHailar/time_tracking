from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.project_user import ProjectUserORM
from app.db.session import database
from app.exceptions import NotFoundError
from app.schemas.project_user import ProjectUserCreateSchema


class ProjectUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_user_to_project(
        self, project_user: ProjectUserCreateSchema
    ) -> ProjectUserORM:
        new_entry = ProjectUserORM(**project_user.model_dump())
        self.db.add(new_entry)
        try:
            await self.db.flush()
            return new_entry
        except IntegrityError as err:
            raise ValueError("User already added to this project.") from err

    async def remove_user_from_project(self, user_id: int, project_id: int) -> None:
        query = select(ProjectUserORM).where(
            ProjectUserORM.user_id == user_id, ProjectUserORM.project_id == project_id
        )
        result = await self.db.execute(query)
        entry = result.scalars().first()
        if not entry:
            raise NotFoundError("There is no current user in current project.")
        await self.db.delete(entry)
        await self.db.flush()

    async def get_project_users(self, project_id: int) -> List[ProjectUserORM]:
        query = select(ProjectUserORM).where(ProjectUserORM.project_id == project_id)
        result = await self.db.execute(query)
        return result.scalars().all()


def get_project_users_repository(
    db: Annotated[AsyncSession, Depends(database.get_db)],
) -> ProjectUserRepository:
    return ProjectUserRepository(db)
