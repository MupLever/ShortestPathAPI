from typing import Optional
from sqlalchemy.orm import Session

from app.models import User


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.query(User).where(User.username == username).first()
