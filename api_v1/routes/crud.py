from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import List, Dict, Any, Optional, Type

from app.models import Route, User, Position, Address


def get_routes(session: Session, user: User) -> List[Route]:
    query = (
        select(Route)
        .where(Route.user_id == user.id)
        .options(selectinload(Route.positions).joinedload(Position.address))
    )
    return list(session.execute(query).scalars().all())


def get_route(session: Session, user: User, route_id: int) -> Optional[Route]:
    query = (
        select(Route)
        .where(Route.id == route_id)
        .where(Route.user_id == user.id)
        .options(selectinload(Route.positions).joinedload(Position.address))
    )
    return session.execute(query).scalars().first()


def create_route(session: Session, user: User, data: Dict[str, Any]) -> Route:
    path = data.pop("path")
    route = Route(**data)
    for pos, node in enumerate(path):
        route.positions.append(
            Position(duration=node["duration"], pos=pos, address_id=node["address"])
        )

    user.routes.append(route)
    session.commit()
    session.refresh(route)
    return route


def delete_route(session: Session, route: Route) -> Route:
    session.delete(route)
    session.commit()
    return route


# TODO: переделать
def update_route(session: Session, route: Route, data_update: Dict[str, Any]) -> Route:
    for name, value in data_update.items():
        setattr(route, name, value)

    session.commit()
    session.refresh(route)
    return route
