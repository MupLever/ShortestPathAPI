from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import User
from api_v1.users.schemas import UserCreate, UserUpdate


def get_user(session: Session, user_id: int) -> User:
    stmt = f"""
    SELECT * 
    FROM users
    WHERE users.id = {user_id};
    """
    return session.query(User).from_statement(text(stmt)).first()


def get_users(session: Session) -> List[User]:
    return session.query(User).from_statement(text("SELECT *FROM users;")).all()


def create_user(session: Session, user_in: UserCreate):
    user = User(**user_in.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user: User, user_update: UserUpdate):
    for name, value in user_update.model_dump().items():
        setattr(user, name, value)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()
    return user
