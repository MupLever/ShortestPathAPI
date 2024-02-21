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

    def __hash__(self):
        return hash(f"{self.city}, {self.street}, {self.house_number}, {self.apartment_number}")

    def __repr__(self):
        return (
            f"{self.city}, {self.street}, {self.house_number}, {self.apartment_number}"
        )

    def __str__(self):
        return self.__repr__()


class LegalAddress(LegalAddressBase):
    pass
    # id: int


class LegalAddressesCreate(LegalAddressBase):
    pass
