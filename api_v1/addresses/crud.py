from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session

from api_v1.addresses.schemas import LegalAddress
from app.models import Address


def get_address_by_part(session: Session, part: LegalAddress) -> List[Address]:
    stmt = """SELECT street FROM (
    SELECT city, district, street FROM addresses
    WHERE district LIKE 'Акад%'
    GROUP BY city, district, street) AS TMP;
    """
    return session.query(Address).from_statement(text(stmt)).all()
