from pydantic import BaseModel, Field

from app.types import Category


class ExecutorCreate(BaseModel):
    fullname: str = Field(pattern=r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$")
    age: int = Field(gt=0, lt=200)
    category: Category
    phone_number: str = Field(pattern=r"^(8|\+7)9{9}$")
    passport: str = Field(pattern=r"^\d{4}\s?\d{6}$")
