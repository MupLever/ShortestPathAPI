import enum

from datetime import datetime
from typing import Optional, List

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
)


class Status(enum.Enum):
    pending = "pending"
    done = "done"
    canceled = "canceled"


def model_dump(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"



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

    routes: Mapped[List["Route"]] = relationship(
        back_populates="addresses", secondary="positions"
    )
    positions: Mapped[List["Position"]] = relationship(back_populates="address")


class Geocoordinates(Base):
    __tablename__ = "geocoordinates"

    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE")
    )


class Route(Base):
    __tablename__ = "routes"

    total_duration: Mapped[int] = mapped_column(nullable=False)
    executor: Mapped[str] = mapped_column(nullable=False)
    execution_date: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="routes")

    positions: Mapped[List["Position"]] = relationship(back_populates="route")
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="routes", secondary="positions"
    )


class Position(Base):
    __tablename__ = "positions"

    duration: Mapped[int] = mapped_column(nullable=False)
    pos: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(server_default=text("'pending'"))
    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE")
    )
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id", ondelete="CASCADE")
    )

    route: Mapped["Route"] = relationship(back_populates="positions")
    address: Mapped["Address"] = relationship(back_populates="positions")
