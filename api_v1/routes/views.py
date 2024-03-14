from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.addresses.crud import get_addresses_by_id_list
from api_v1.routes import crud
from api_v1.auth.utils import get_current_user
from api_v1.routes.schemas import Info
from api_v1.routes.utils import graph_api, external_api
from app.models import User

from configs.database import get_session_dependency

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
    session: Session = Depends(get_session_dependency),
):
    if len(info.addresses_ids) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the number of vertices is less than 3",
        )

    legal_addresses = get_addresses_by_id_list(session, info.addresses_ids)
    coordinates_dict = external_api.get_coordinates(legal_addresses)
    edges_list = external_api.get_distances(coordinates_dict)
    data = graph_api.get_min_hamiltonian_cycle(edges_list)
    data["executor"] = info.executor
    data["execution_date"] = info.execution_date

    route = crud.create_route(session, user, data)
    msg = "SUCCESS: The shortest path has been successfully found"
    return {"message": msg, "shortest_path": route}


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
# @router.put("/{route_id}/", description="Изменить маршрут")
# async def update_route(
#         route_id: int,
#         info: Info,
#         user: User = Depends(get_current_user),
#         session: Session = Depends(get_session_dependency),
# ):
#     route = crud.get_route(session, user, route_id)
#
#     if not route:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Route with {route_id=} not found",
#         )
#
#     if len(legal_addresses) < 3:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="the number of vertices is less than 3",
#         )
#
#     legal_addresses = get_addresses_by_id_list(session, info.addresses_ids)
#     coordinates_dict = external_api.get_coordinates(legal_addresses)
#     edges_list = external_api.get_distances(coordinates_dict)
#     data = graph_api.get_min_hamiltonian_cycle(edges_list)
#     data["executor"] = info.executor
#     data["execution_date"] = info.execution_date
#
#     new_route = crud.update_route(session, route, data)
#     msg = "SUCCESS: The shortest path has been successfully found"
#
#     return {"message": msg, "shortest_path": new_route}
