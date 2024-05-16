from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload

from app.models import Product, Order, User
from app.types import Category, Status


def create(session: Session, user: User, order_dict: dict) -> Order:
    products = map(lambda _product: Product(**_product), order_dict.pop("products"))

    order_dict["user_id"] = user.id
    order = Order(**order_dict)
    for product in products:
        order.products.append(product)

    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_orders(session: Session, user: User, date: datetime, category: Category) -> List[Order]:
    stmt = (
        select(Order)
        .where(Order.user_id == user.id)
        .where(func.date(Order.expected_date) == date.date())
        .where((Order.status == Status.pending))
        .options(joinedload(Order.address))
        .options(selectinload(Order.products))
    )
    orders = list(session.execute(stmt).scalars().all())

    check = all if category == Category.lightweight else any

    category_orders = [
        order
        for order in orders
        if check([product.category == category for product in order.products])
    ]

    return category_orders


def get_order(session: Session, user: User, order_id: int) -> Optional[Order]:
    query = (
        select(Order)
        .where(Order.user_id == user.id)
        .where(Order.id == order_id)
        .options(joinedload(Order.address))
        .options(selectinload(Order.products))
    )
    return session.execute(query).scalars().first()


def update_status(session: Session, order: Order, status: Status) -> Order:
    order.status = status
    session.commit()
    session.refresh(order)
    return order
