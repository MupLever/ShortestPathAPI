from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import User
from api_v1.users.schemas import UserCreate, UserUpdate
from utils import auth


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).where(User.id == user_id).first()


def get_users(session: Session) -> List[User]:
    return session.query(User).from_statement(text("SELECT * FROM users;")).all()


def create_user(session: Session, user_in: UserCreate) -> User:
    tmp_user = user_in.model_dump()
    tmp_user["password"] = auth.hash_password(tmp_user["password"])
    user = User(**tmp_user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user: User, user_update: UserUpdate) -> User:
    for name, value in user_update.model_dump().items():
        setattr(user, name, value)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User) -> User:
    session.delete(user)
    session.commit()
    return user
