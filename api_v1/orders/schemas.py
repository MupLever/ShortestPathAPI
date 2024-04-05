from datetime import datetime
from typing import List

from pydantic import BaseModel

from configs.settings import Category


class Product(BaseModel):
    name: str
    category: Category
    count: int
    weight: float
    article_number: int
    hazard_class: int
    expiration_date: datetime


class OrderCreate(BaseModel):
    products: List[Product]
    client: str
    expected_date: datetime
    address_id: int
