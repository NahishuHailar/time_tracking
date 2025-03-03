from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: int) -> Project:
        return await self.db.get(Project, project_id)

    async def create(self, project_data: ProjectCreate) -> Project:
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update(self, project_id: int, project_data: ProjectUpdate) -> Project:
        project = await self.get_by_id(project_id)
        if project:
            for key, value in project_data.model_dump().items():
                setattr(project, key, value)
            await self.db.commit()
            await self.db.refresh(project)
        return project

    async def delete(self, project_id: int) -> bool:
        project = await self.get_by_id(project_id)
        if project:
            await self.db.delete(project)
            await self.db.commit()
            return True
        return False