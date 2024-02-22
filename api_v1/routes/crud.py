from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Route, User


def get_routes(session: Session) -> List[Route]:
    user_id = 2
    return (
        session.query(Route)
        .join(User, User.id == Route.user_id)
        .where(User.id == user_id)
        .all()
    )


def get_route(session: Session, route_id: int) -> Optional[Route]:
    user_id = 2
    return (
        session.query(Route)
        .join(User, User.id == Route.user_id)
        .where(User.id == user_id)
        .where(Route.id == route_id)
        .first()
    )


def create_route(session: Session, data: Dict[str, Any]) -> Route:
    route = Route(**data)
    session.add(route)
    session.commit()
    session.refresh(route)
    return route


def delete_route(session: Session, route: Route) -> Route:
    session.delete(route)
    session.commit()
    return route


def update_route(session: Session, route: Route, data_update: Dict[str, Any]) -> Route:
    for name, value in data_update.items():
        setattr(route, name, value)
    session.commit()
    session.refresh(route)
    return route
