from fastapi import APIRouter, Depends
from services.project import ProjectService
from schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectSchema

router = APIRouter()

@router.post("/projects/", response_model=ProjectSchema)
async def create_project(
    project_data: ProjectCreateSchema,
    project_service: ProjectService = Depends(ProjectService),
):
    return await project_service.create_project(project_data)

@router.get("/projects/{project_id}", response_model=ProjectSchema)
async def read_project(
    project_id: int,
    project_service: ProjectService = Depends(ProjectService),
):
    return await project_service.get_project(project_id)

@router.put("/projects/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    project_data: ProjectUpdateSchema,
    project_service: ProjectService = Depends(ProjectService),
):
    return await project_service.update_project(project_id, project_data)

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(ProjectService),
):
    await project_service.delete_project(project_id)
    return {"message": "Project deleted"}