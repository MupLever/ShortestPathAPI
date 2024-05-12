import asyncio
from typing import List, Type, Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload

from app.models import Address, Order
from configs.settings import Status


def get_address_by_part(session: Session, part_address: str) -> List[Type[Address]]:
    columns = (Address.district, Address.city, Address.street, Address.house_number)
    values = part_address.split(" ")
    filters = [column.startswith(value) for column in columns for value in values]

    stmt = select(Address.id, *columns).where(or_(*filters)).limit(6)

    return session.query(Address).from_statement(stmt).all()


def get_address_by_id(session: Session, address_id: int) -> Optional[Address]:
    return session.query(Address).get(address_id)


def get_orders_by_order_id_list(
    session: Session, orders_identifiers: List[int]
) -> List[Type[Order]]:
    orders = (
        session.query(Order)
        .options(joinedload(Order.address))
        .where(Order.id.in_(orders_identifiers))
        .all()
    )
    # for order in orders:
    #     order.status = Status.done
    #
    # session.commit()
    # session.refresh(orders)
    return orders
