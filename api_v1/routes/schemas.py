from datetime import datetime
from typing import List

from pydantic import BaseModel

from configs.settings import Category


class Geocoordinates(BaseModel):
    lat: str
    lng: str


class Info(BaseModel):
    orders_ids: List[int]
    category: Category
    executor_id: int
    execution_date: datetime
