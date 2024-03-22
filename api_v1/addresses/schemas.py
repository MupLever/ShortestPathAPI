from typing import Optional

from pydantic import BaseModel


class LegalAddress(BaseModel):
    city: str
    district: Optional[str]
    street: Optional[str]
    house_number: Optional[str]
