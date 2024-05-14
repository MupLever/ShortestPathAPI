from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.types import Category


class Product(BaseModel):
    name: str
    category: Category
    count: int
    weight: float
    article_number: int
    hazard_class: int
    expiration_date: datetime


class OrderCreate(BaseModel):
    number: int
    client: str
    expected_date: datetime
    address_id: int
    products: List[Product]
