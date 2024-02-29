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

    def __repr__(self):
        return (
            f"{self.city}, {self.district}, {self.street}, "
            f"{self.house_number}, {self.apartment_number}"
        )

    def __hash__(self):
        return hash(self.__repr__())

    def __str__(self):
        return self.__repr__()


class LegalAddress(LegalAddressBase):
    pass
    # id: int
