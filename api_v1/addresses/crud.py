from typing import List, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from api_v1.addresses.schemas import LegalAddress
from app.models import Address


def get_address_by_part(session: Session, part: LegalAddress) -> List[Type[Address]]:
    stmt = select(
        Address.id, Address.city, Address.district, Address.street, Address.house_number
    )
    for name, value in part.model_dump(exclude_none=True).items():
        stmt = stmt.where(getattr(Address, name).startswith(value))

    addresses = session.query(Address).from_statement(stmt).all()
    return addresses


def get_addresses_by_id_list(
    session: Session, addresses_identifiers: List[int]
) -> List[Type[Address]]:
    return session.query(Address).where(Address.id.in_(addresses_identifiers)).all()
