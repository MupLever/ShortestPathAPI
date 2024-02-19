from pydantic import EmailStr
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
