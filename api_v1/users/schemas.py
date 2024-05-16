from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=6)
    email: EmailStr
    password: str = Field(min_length=6)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass
