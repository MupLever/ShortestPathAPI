# schemas
class LegalAddress:
    city: str
    district: str
    street: str
    house_number: str
    apartment_number: int
    entrance_number: int
    floor: int
    latitude: float
    longitude: float


class Path:
    id: int
    duration: float
    distance: float


class LegalAddressPath:
    index: int
    path_id: int
    legal_address_id: int
