from typing import Dict, Any

from pydantic import BaseModel


class Geocoordinates(BaseModel):
    lat: int
    lng: int


class LegalAddressBase(BaseModel):
    city: str
    district: str
    street: str
    house_number: str
    apartment_number: int
    entrance_number: int
    floor: int

    def __repr__(self):
        return (
            f"{self.city}, {self.district}, {self.street}, "
            f"{self.house_number}, {self.apartment_number}, {self.entrance_number}, {self.floor}"
        )

    def __hash__(self):
        return hash(
            self.__repr__()
        )

    def __str__(self):
        return self.__repr__()


class LegalAddress(LegalAddressBase):
    pass
    # id: int


class LegalAddressCreate(LegalAddressBase):
    pass


class LegalAddressUpdate(LegalAddressBase):
    pass


# class RouteBase(BaseModel):
#     id: int
#     total_duration: int
#     path: Dict[str, Any]
#     user_id: int
