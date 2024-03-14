from datetime import datetime
from typing import List

from pydantic import BaseModel


class Geocoordinates(BaseModel):
    lat: int
    lng: int


class Info(BaseModel):
    addresses_ids: List[int]
    executor: str
    execution_date: datetime
