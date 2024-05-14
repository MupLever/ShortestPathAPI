from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.types import Category


class Geocoordinates(BaseModel):
    lat: str
    lng: str


class Info(BaseModel):
    address_id: int = Field(gt=0)
    orders_ids: List[int]
    category: Category
    executor_id: int = Field(gt=0)
    execution_date: datetime
