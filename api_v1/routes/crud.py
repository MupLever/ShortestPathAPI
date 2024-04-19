from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List, Dict, Any, Optional

from app.models import Route, User, Position, Order


def get_routes(session: Session, user: User) -> List[Route]:
    query = (
        select(Route)
        .where(Route.user_id == user.id)
        .options(
            selectinload(Route.positions)
            .joinedload(Position.order)
            .joinedload(Order.address)
        )
    )
    return list(session.execute(query).scalars().all())


def get_route(session: Session, user: User, route_id: int) -> Optional[Route]:
    query = (
        select(Route)
        .where(Route.id == route_id)
        .where(Route.user_id == user.id)
        .options(
            selectinload(Route.positions)
            .joinedload(Position.order)
            .joinedload(Order.address)
        )
    )
    return session.execute(query).scalars().first()


def create_route(session: Session, user: User, data: Dict[str, Any]) -> Route:
    path = data.pop("path")
    route = Route(**data)
    for pos, node in enumerate(path):
        route.positions.append(
            Position(duration=node["duration"], transport=node["transport"], pos=pos, order_id=node["node"])
        )

    user.routes.append(route)
    session.commit()
    session.refresh(route)
    return route


def delete_route(session: Session, route: Route) -> Route:
    session.delete(route)
    session.commit()
    return route
