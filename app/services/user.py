from typing import Annotated, Optional

from db.repositories.user import UserRepository, get_user_repository
from fastapi import Depends
from schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> Optional[UserSchema]:
        return await self.user_repository.get_by_id(user_id)

    async def create_user(self, user_data: UserCreateSchema) -> UserSchema:
        return await self.user_repository.create(user_data)

    async def update_user(
        self, user_id: int, user_data: UserUpdateSchema
    ) -> UserSchema:
        return await self.user_repository.update(user_id, user_data)

    async def delete_user(self, user_id: int) -> None:
        return await self.user_repository.delete(user_id)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)
