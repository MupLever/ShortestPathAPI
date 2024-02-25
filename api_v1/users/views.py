from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from api_v1.auth.utils import get_current_user
from api_v1.users import crud
from api_v1.users.schemas import UserCreate, UserUpdate
from app.models import User
from configs.database import get_session_dependency

router = APIRouter(tags=["Users"], prefix="/api/v1/shortest_path/users")


@router.post("/", description="Создать пользователя")
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session_dependency)
):
    return crud.create_user(session, user)


@router.get("/{user_id}/", description="Получить пользователя по идентификатору")
async def get_user(user_id: int, session: Session = Depends(get_session_dependency)):
    user = crud.get_user(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} not found",
        )

    return user


@router.get("/", description="Получить всех пользователей")
async def get_users(session: Session = Depends(get_session_dependency)):
    return crud.get_users(session)


@router.delete("/{user_id}/", description="Удалить пользователя")
async def delete_user(
        user_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session_dependency),
):
    user = crud.get_user(session, user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} not found",
        )

    return crud.delete_user(session, user)


@router.put("/{user_id}/", description="Редактировать пользователя")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    user = crud.get_user(session, user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} not found",
        )

    return crud.update_user(session, user, user_update)
