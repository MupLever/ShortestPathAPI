from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass
