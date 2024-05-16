from typing import List, Type, Optional

from sqlalchemy.orm import Session

from api_v1.executors.schemas import ExecutorCreate
from app.models import Executor, User
from app.types import Category


def create(session: Session, user: User, executor: ExecutorCreate) -> Executor:
    executor_dict = executor.model_dump()
    executor_dict["user_id"] = user.id
    executor = Executor(**executor_dict)
    session.add(executor)
    session.commit()
    session.refresh(executor)
    return executor


def get_executors(session: Session, user: User) -> List[Type[Executor]]:
    return list(
        session
        .query(Executor)
        .where(Executor.user_id == user.id)
        .where(Executor.is_active)
        .all()
    )


def get_executors_by_filters(
    session: Session, user: User, category: Category, part_fullname: str
) -> List[Type[Executor]]:
    return list(
        session.query(Executor)
        .where(Executor.user_id == user.id)
        .where(Executor.fullname.startswith(part_fullname))
        .where(Executor.category == category)
        .where(Executor.is_active)
        .limit(6)
        .all()
    )


def get_executor(session: Session, user: User, executor_id: int) -> Optional[Executor]:
    return (
        session.query(Executor)
        .where(Executor.user_id == user.id)
        .where(Executor.id == executor_id)
        .where(Executor.is_active)
        .first()
    )


def dismiss(session: Session, executor: Executor) -> Optional[Executor]:
    executor.is_active = False
    session.commit()
    return executor
