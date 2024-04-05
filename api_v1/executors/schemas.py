from pydantic import BaseModel

from configs.settings import Category


class ExecutorCreate(BaseModel):
    fullname: str
    category: Category
