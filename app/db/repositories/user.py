from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import UserORM
from db.session import database
from exceptions import NotFoundError
from schemas.user import UserCreateSchema, UserUpdateSchema
from typing import List, Optional


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(database.get_db)):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[UserORM]:
        user = await self.db.get(UserORM, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def create(self, user_data: UserCreateSchema) -> UserORM:
        user = UserORM(**user_data.model_dump())
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdateSchema) -> UserORM:
        user = await self.get_by_id(user_id)
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.db.delete(user)
        await self.db.flush()
