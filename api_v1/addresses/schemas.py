from pydantic import BaseModel


class LegalAddressBase(BaseModel):
    city: str
    district: str
    street: str
    house_number: int
    apartment_number: int
    entrance_number: int
    floor: int


class LegalAddress(LegalAddressBase):
    pass
    # id: int


class LegalAddressCreate(LegalAddressBase):
    pass


class LegalAddressUpdate(LegalAddressBase):
    pass
