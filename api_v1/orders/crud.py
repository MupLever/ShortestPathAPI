from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from api_v1.orders.schemas import OrderCreate
from app.models import Product, Order


def create(session: Session, order_dict: dict) -> Order:
    products = map(lambda product: Product(**product), order_dict.pop("products"))
    order = Order(**order_dict)
    for product in products:
        order.products.append(product)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_orders(session: Session) -> List[Order]:
    query = (
        select(Order)
        .options(selectinload(Order.products))
    )
    return list(session.execute(query).scalars().all())


def get_order(session: Session, order_id: int) -> Optional[Order]:
    query = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.products))
    )
    return session.execute(query).scalars().first()


def delete(session: Session, order: Order) -> Order:
    pass
