from sqlalchemy.orm import Session
from typing import List, Optional, Type

from app.models import User
from api_v1.users.schemas import UserCreate, UserUpdate
from utils import auth


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).where(User.id == user_id).first()


def get_users(session: Session) -> List[Type[User]]:
    return session.query(User).all()


def create_user(session: Session, user_in: UserCreate) -> User:
    user_in_dict = user_in.model_dump()
    user_in_dict["password"] = auth.hash_password(user_in_dict["password"]).decode()
    user = User(**user_in_dict)
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
    user.is_active = False
    # session.delete(user)
    session.commit()
    return user
