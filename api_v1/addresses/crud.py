from typing import List, Type

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models import Address


def get_address_by_part(session: Session, part_address: str) -> List[Type[Address]]:
    columns = (Address.district, Address.city, Address.street, Address.house_number)
    values = part_address.split(" ")
    filters = [column.startswith(value) for column in columns for value in values]

    stmt = select(Address.id, *columns).where(or_(*filters)).limit(6)

    return session.query(Address).from_statement(stmt).all()


def get_addresses_by_id_list(
    session: Session, addresses_identifiers: List[int]
) -> List[Type[Address]]:
    return session.query(Address).where(Address.id.in_(addresses_identifiers)).all()
