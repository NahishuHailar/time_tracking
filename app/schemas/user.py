from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    # email: str
    # full_name: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    pass
    # password: str


class UserUpdateSchema(UserBaseSchema):
    pass
    # full_name: Optional[str] = None


class UserSchema(UserBaseSchema):
    id: int
    # created_at: datetime

    class Config:
        from_attributes = True
