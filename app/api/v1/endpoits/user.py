from fastapi import APIRouter, Depends
from services.user import UserService
from schemas.user import UserCreateSchema, UserUpdateSchema, UserSchema

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(UserService),
):
    return await user_service.create_user(user_data)

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    user_service: UserService = Depends(UserService),
):
    return await user_service.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    user_service: UserService = Depends(UserService),
):
    return await user_service.update_user(user_id, user_data)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(UserService),
)-> dict:
    await user_service.delete_user(user_id)
    return {"message": "User deleted"}
