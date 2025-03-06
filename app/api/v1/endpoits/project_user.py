from fastapi import APIRouter, Depends
from schemas.project_user import ProjectUserCreateSchema, ProjectUserSchema
from services.project_user import ProjectUserService, get_project_users_service

router = APIRouter()


@router.post("/add_user", response_model=ProjectUserSchema)
async def add_user_to_project(
    project_user_data: ProjectUserCreateSchema,
    project_user_service: ProjectUserService = Depends(get_project_users_service),
):
    return await project_user_service.add_user_to_project(project_user_data)


@router.delete("/{user_id}/{project_id}")
async def remove_user(
    user_id: int,
    project_id: int,
    project_user_service: ProjectUserService = Depends(get_project_users_service),
):
    return await project_user_service.remove_user(user_id, project_id)
