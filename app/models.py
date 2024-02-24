from datetime import datetime
from typing import Any, Dict

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import (
    MetaData,
    text,
    Table,
    Column,
    Integer,
    String,
    Float,
    JSON,
    TIMESTAMP,
    ForeignKey,
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class Address(Base):
    __tablename__ = "addresses"

    city: Mapped[str] = mapped_column(nullable=False)
    district: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[str] = mapped_column(nullable=False)
    apartment_number: Mapped[str] = mapped_column()
    entrance_number: Mapped[int] = mapped_column()
    floor: Mapped[int] = mapped_column()


class Geocoordinates(Base):
    __tablename__ = "geocoordinates"

    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE")
    )


class AddressRoute(Base):
    __tablename__ = "address_route"

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))


class Route(Base):
    __tablename__ = "routes"

    total_duration: Mapped[int] = mapped_column(nullable=False)
    path: Mapped[Dict[str, Any]] = mapped_column(type_=JSON, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
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
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)

geocoordinates = Table(
    "geocoordinates",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("address_id", ForeignKey("addresses.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)

routes = Table(
    "routes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("total_duration", Integer, nullable=False),
    Column("path", JSON, nullable=False),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)

address_route = Table(
    "address_route",
    metadata,
    Column("address_id", ForeignKey("addresses.id", ondelete="CASCADE")),
    Column("route_id", ForeignKey("routes.id", ondelete="CASCADE")),
)
