from fastapi import APIRouter, Depends
from app.services.project_user import ProjectUserService
from app.schemas.project_user import ProjectUserCreateSchema, ProjectUserSchema
from typing import List


router = APIRouter()


@router.post("/add_user", response_model=ProjectUserSchema)
async def add_user_to_project(
    project_user_data: ProjectUserCreateSchema,
    project_user_service: ProjectUserService = Depends(ProjectUserService),
):
    return await project_user_service.add_user_to_project(project_user_data)


@router.delete("/{user_id}/{project_id}")
async def remove_user(
    user_id: int, project_id: int,  
    project_user_service: ProjectUserService = Depends(ProjectUserService)):
    return await project_user_service.remove_user(user_id, project_id)

