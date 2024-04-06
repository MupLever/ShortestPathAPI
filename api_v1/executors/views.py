from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.auth.utils import get_current_user
from api_v1.executors import crud
from api_v1.executors.schemas import ExecutorCreate
from app.models import User
from configs.database import get_session_dependency
from configs.settings import Category

router = APIRouter(tags=["Executors"], prefix="/api/v1/shortest_path/executors")


@router.get("/", description="")
async def get_executors_by(
    part_fullname: str,
    category: Category,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_executors_by(session, category, part_fullname)


@router.get("/", description="")
async def get_executors(
    category: Category,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_executors(session, category)


@router.post("/", description="")
async def create_executor(
    executor: ExecutorCreate,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.create(session, executor)


@router.delete("/{executor_id}/", description="")
async def dismiss_executor(
    executor_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    executor = crud.get_executor(session, executor_id)
    if not executor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Executor with {executor_id=} not found",
        )

    return crud.dismiss(session, executor)
