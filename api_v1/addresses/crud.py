from typing import List, Type
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_v1.addresses.schemas import LegalAddress
from app.models import Address


def get_address_by_part(session: Session, part: LegalAddress) -> List[Type[Address]]:
    stmt = select(Address)
    for name, value in part.model_dump(exclude_none=True).items():
        stmt = stmt.where(getattr(Address, name).startswith(value))

    addresses = session.query(Address).from_statement(stmt).all()
    return addresses
