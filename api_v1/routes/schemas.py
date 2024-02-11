from datetime import datetime
from pydantic import BaseModel


class Geocoordinates(BaseModel):
    lat: int
    lng: int


class LegalAddressBase(BaseModel):
    city: str
    # district: str
    street: str
    house_number: int
    apartment_number: int
    entrance_number: int
    floor: int

    def __repr__(self):
        return (
            f"{self.city}, {self.street}, {self.house_number}, {self.apartment_number}"
        )

    def __str__(self):
        return self.__repr__()


class LegalAddress(LegalAddressBase):
    pass


class LegalAddressesCreate(LegalAddressBase):
    id: int
    deleted: bool
    created_at: datetime
    updated_at: datetime
