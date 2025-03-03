from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database
from app.services.project import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, Project

router = APIRouter()

@router.post("/projects/", response_model=Project)
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(database.get_db)):
    project_service = ProjectService(ProjectRepository(db))
    return await project_service.create_project(project_data)

@router.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: int, db: AsyncSession = Depends(database.get_db)):
    project_service = ProjectService(ProjectRepository(db))
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(database.get_db)):
    project_service = ProjectService(ProjectRepository(db))
    project = await project_service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(database.get_db)):
    project_service = ProjectService(ProjectRepository(db))
    success = await project_service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}