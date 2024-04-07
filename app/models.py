from datetime import datetime
from typing import Optional, List

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
)

from configs.settings import Status, Category


def model_dump(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=text("True"))
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )

    routes: Mapped[List["Route"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    city: Mapped[str] = mapped_column(nullable=False)
    district: Mapped[Optional[str]] = mapped_column()
    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[str] = mapped_column(nullable=False)

    # routes: Mapped[List["Route"]] = relationship(
    #     back_populates="addresses", secondary="positions"
    # )

    orders: Mapped[List["Order"]] = relationship(back_populates="address")
    # positions: Mapped[List["Position"]] = relationship(back_populates="address")


class Route(Base):
    __tablename__ = "routes"

    total_duration: Mapped[int] = mapped_column(nullable=False)
    execution_date: Mapped[datetime] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    executor_id: Mapped[int] = mapped_column(ForeignKey("executors.id"))

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="routes")
    executor: Mapped["Executor"] = relationship(back_populates="routes")
    positions: Mapped[List["Position"]] = relationship(back_populates="route")


class Position(Base):
    __tablename__ = "positions"

    duration: Mapped[int] = mapped_column(nullable=False)
    pos: Mapped[int] = mapped_column(nullable=False)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"))

    route: Mapped["Route"] = relationship(back_populates="positions")
    order: Mapped["Order"] = relationship(back_populates="position")


class Executor(Base):
    __tablename__ = "executors"

    fullname: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[Category] = mapped_column(nullable=False)
    workload: Mapped[bool] = mapped_column(nullable=False, server_default=text("False"))
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text("True"))

    routes: Mapped[List["Route"]] = relationship(back_populates="executor")


class Order(Base):
    __tablename__ = "orders"

    number: Mapped[int] = mapped_column(nullable=False)
    client: Mapped[str] = mapped_column(nullable=False)
    expected_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(server_default=text("'pending'"))

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))

    position: Mapped["Position"] = relationship(back_populates="order")
    products: Mapped[List["Product"]] = relationship(back_populates="order")
    address: Mapped["Address"] = relationship(back_populates="orders")


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[Category] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    article_number: Mapped[int] = mapped_column(nullable=False)
    hazard_class: Mapped[int] = mapped_column(nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))

    order: Mapped["Order"] = relationship(back_populates="products")


# class Geocoordinates(Base):
#     __tablename__ = "geocoordinates"
#
#     latitude: Mapped[float] = mapped_column()
#     longitude: Mapped[float] = mapped_column()
#
#     address_id: Mapped[int] = mapped_column(
#         ForeignKey("addresses.id", ondelete="CASCADE")
#     )
