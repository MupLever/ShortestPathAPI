from typing import Optional

from pydantic import BaseModel, ConfigDict


class LegalAddressBase(BaseModel):
    city: str
    district: Optional[str]
    street: Optional[str]
    house_number: Optional[str]
    apartment_number: Optional[int]


class LegalAddress(LegalAddressBase):
    pass
    # id: int

