from typing import List, Type, Optional

from sqlalchemy.orm import Session

from api_v1.executors.schemas import ExecutorCreate
from app.models import Executor
from configs.settings import Category


def create(session: Session, executor: ExecutorCreate) -> Executor:
    executor = Executor(**executor.model_dump())
    session.add(executor)
    session.commit()
    session.refresh(executor)
    return executor


def get_executors(session: Session, category: Category) -> List[Type[Executor]]:
    return list(
        session.query(Executor)
        .where(Executor.is_active)
        .where(Executor.category == category)
        .all()
    )


def get_executor(session: Session, executor_id: int) -> Optional[Executor]:
    return (
        session.query(Executor)
        .where(Executor.id == executor_id)
        .where(Executor.is_active)
        .first()
    )


def get_executors_by(
        session: Session, category: Category, part_fullname: str
) -> List[Type[Executor]]:
    return list(
        session.query(Executor)
        .where(Executor.fullname.startswith(part_fullname))
        .where(Executor.category == category)
        .where(Executor.is_active)
        .limit(6)
        .all()
    )


def dismiss(session: Session, executor: Executor) -> Optional[Executor]:
    executor.is_active = False
    session.commit()
    return executor
