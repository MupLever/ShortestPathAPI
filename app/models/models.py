from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column
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

from configs.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[EmailStr] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


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
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_duration: Mapped[int] = mapped_column(nullable=False)
    path: Mapped[dict] = mapped_column(nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", EmailStr, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", server_default=text("TIMEZONE('utc', now())")),
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
    Column("latitude", Float),
    Column("longitude", Float),
    Column("item_id", ForeignKey("items.id")),
    Column("created_at", server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("created_at", server_default=text("TIMEZONE('utc', now())")),
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
    Column("item_id", ForeignKey("items.id")),
    Column("created_at", server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)
