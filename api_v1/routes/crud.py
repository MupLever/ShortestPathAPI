from typing import List

from sqlalchemy import Result, text
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession


def create_route(session: Session):
    pass


def get_routes(session: Session):
    query = """
    SELECT * 
    FROM users INNER JOIN items ON users.id = routes.user_id;
    """

    with session as session:
        result: Result = session.execute(text(query))
        routes = result.scalars().all()
        return list(routes)


def get_route(session: Session, route_id: int):
    query = f"""
        SELECT * 
        FROM users INNER JOIN items ON users.id = routes.user_id
    	WHERE routes.id = {route_id};
        """

    with session as session:
        result: Result = session.execute(text(query))
        return result.scalar()


def delete_route(session: Session):
    pass


def update_route(session: Session):
    pass
