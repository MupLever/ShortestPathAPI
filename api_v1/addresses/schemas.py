from typing import Optional

from pydantic import BaseModel


# TODO: можно удалять наверн
class LegalAddress(BaseModel):
    city: str
    district: Optional[str]
    street: Optional[str]
    house_number: Optional[str]
