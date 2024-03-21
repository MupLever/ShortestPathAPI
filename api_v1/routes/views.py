from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.routes import crud
from api_v1.auth.utils import get_current_user
from api_v1.routes.schemas import Info
from app.models import User
from configs.database import get_session_dependency
from tasks import route as route_task

router = APIRouter(tags=["Routes"], prefix="/api/v1/shortest_path/routes")


@router.get("/", description="Список маршрутов")
async def get_routes(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_routes(session, user)


@router.get("/{route_id}/", description="Получить маршрут по идентификатору")
async def get_route(
    route_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_route(session, user, route_id)


@router.post("/", description="Добавить маршрут")
async def create_shortest_path(
    info: Info,
    user: User = Depends(get_current_user),
):
    if len(info.addresses_ids) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the number of vertices is less than 3",
        )

    route_task.create.delay(info.model_dump(), user.id)

    return {"message": "Success: the request has been accepted for processing"}


@router.delete("/{route_id}/", description="Удалить маршрут")
async def delete_route(
    route_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    route = crud.get_route(session, user, route_id)

    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with {route_id=} not found",
        )
    return crud.delete_route(session, route)


# TODO: переделать
# @router.patch("/{route_id}/", description="Изменить статус продвижения по маршруту")
async def update_route_status(
        route_id: int,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session_dependency),
):
    route = crud.get_route(session, user, route_id)

    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with {route_id=} not found",
        )

    return {}
