from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Route, User


def get_routes(session: Session, user: User) -> List[Route]:
    return (
        session.query(Route)
        .join(User, User.id == Route.user_id)
        .where(User.id == user.id)
        .all()
    )


def get_route(session: Session, user: User, route_id: int) -> Optional[Route]:
    return (
        session.query(Route)
        .join(User, User.id == Route.user_id)
        .where(User.id == user.id)
        .where(Route.id == route_id)
        .first()
    )


def create_route(session: Session, user: User, data: Dict[str, Any]) -> Route:
    data["user_id"] = user.id
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
