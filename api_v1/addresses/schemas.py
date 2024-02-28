from typing import Optional

from pydantic import BaseModel


class LegalAddressBase(BaseModel):
    city: str
    district: Optional[str]
    street: Optional[str]
    house_number: Optional[int]
    apartment_number: Optional[int]
    entrance_number: Optional[int]
    floor: Optional[int]


class LegalAddress(LegalAddressBase):
    pass
