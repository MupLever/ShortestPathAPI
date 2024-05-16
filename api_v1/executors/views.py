from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.auth.utils import get_current_user
from api_v1.executors import crud
from api_v1.executors.schemas import ExecutorCreate
from app.models import User
from configs.database import get_session_dependency
from app.types import Category

router = APIRouter(tags=["Executors"], prefix="/api/v1/shortest_path/executors")


@router.get("/", description="")
async def get_executors_by_filters(
    all_: bool,
    category: Category = Category.lightweight,
    part_fullname: str = "",
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    if all_:
        return crud.get_executors(session, user)

    return crud.get_executors_by_filters(session, user, category, part_fullname)


@router.post("/", description="")
async def create_executor(
    executor: ExecutorCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.create(session, user, executor)


@router.delete("/{executor_id}/", description="")
async def dismiss_executor(
    executor_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    executor = crud.get_executor(session, user, executor_id)
    if not executor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Executor with {executor_id=} not found",
        )

    return crud.dismiss(session, executor)
