from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    JSON,
    TIMESTAMP,
    ForeignKey,
)

from configs.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[EmailStr] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=False)
    district: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[str] = mapped_column(nullable=False)
    apartment_number: Mapped[str] = mapped_column()
    entrance_number: Mapped[int] = mapped_column()
    floor: Mapped[int] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Route(Base):
    __tablename__ = "routes"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_duration: Mapped[int] = mapped_column(nullable=False)
    path: Mapped[dict] = mapped_column(nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", EmailStr, nullable=False),
    Column("password", String, nullable=False),
)

addresses = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("city", String, nullable=False),
    Column("district", String),
    Column("street", String, nullable=False),
    Column("house_number", String, nullable=False),
    Column("apartment_number", String),
    Column("entrance_number", Integer),
    Column("floor", Integer),
    Column("latitude", Float),
    Column("longitude", Float),
)

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),

    Column("user_id", ForeignKey("users.id"))
)

routes = Table(
    "routes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("total_duration", Integer, nullable=False),
    Column("path", JSON, nullable=False),
    Column("item_id", ForeignKey("items.id"))
)
