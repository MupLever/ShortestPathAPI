import asyncio
from typing import List, Type

from sqlalchemy import text, select, or_
from sqlalchemy.orm import Session, joinedload

from app.models import Address, Order
from configs.database import session_factory, async_session_factory
from configs.settings import Status


def get_address_by_part(session: Session, part_address: str) -> List[Type[Address]]:
    columns = (Address.district, Address.city, Address.street, Address.house_number)
    values = part_address.split(" ")
    filters = [column.startswith(value) for column in columns for value in values]

    stmt = select(Address.id, *columns).where(or_(*filters))

    return session.query(Address).from_statement(stmt).all()[:6]


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


async def get_version():
    async with async_session_factory() as session:
        res = await session.execute(text("SELECT VERSION();"))
        print(f"{res.first()=}")


if __name__ == "__main__":
    with session_factory() as session:
        res = session.execute(text("SELECT VERSION();"))
        print(f"{res.first()=}")

    asyncio.get_event_loop().run_until_complete(get_version())
