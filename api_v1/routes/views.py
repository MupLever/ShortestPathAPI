from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.routes import crud
from api_v1.auth.utils import get_current_user
from api_v1.routes.schemas import Info
from app.models import User
from configs.database import get_session_dependency
from configs.orm import get_orders_by_order_id_list
from tasks import route as route_task
from utils import external_api, graph_api


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
    route = crud.get_route(session, user, route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with {route_id=} not found",
        )

    return route


@router.post("/", description="Добавить маршрут")
async def create_shortest_path(
    info: Info,
    user: User = Depends(get_current_user),
):
    if len(info.orders_ids) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the number of vertices is less than 3",
        )

    # route_task.create.delay(info.model_dump(), user.id)
    route_task_create(info.model_dump(), user.id)

    return {"message": "Success: the request has been accepted for processing"}


def route_task_create(info: dict, user_id: int) -> None:
    session = next(get_session_dependency())
    user = session.query(User).get(user_id)

    orders = get_orders_by_order_id_list(session, info["orders_ids"])
    coordinates_dict = external_api.get_coordinates(orders)
    edges_list = external_api.get_distances(coordinates_dict, info["category"])
    data = graph_api.get_min_hamiltonian_cycle(edges_list)

    data["executor_id"] = info["executor_id"]
    data["execution_date"] = info["execution_date"]

    crud.create_route(session, user, data)


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
