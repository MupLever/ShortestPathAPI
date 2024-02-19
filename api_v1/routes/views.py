from typing import List
from fastapi import APIRouter

from api_v1.routes.schemas import LegalAddress

from api_v1.routes.utils.graph_api import get_min_hamilton_cycle
from api_v1.routes.utils.external_api import get_coordinates, get_distances

router = APIRouter(tags=["Routes"], prefix="/api/v1/shortest_path/routes")

route_id: int = 0
database: dict = {}


@router.get("/", description="Список маршрутов")
async def get_routes():
    return list(database.values())


@router.post("/", description="Добавить маршрут")
async def get_shortest_path(legal_addresses: List[LegalAddress]):
    coordinates_list = get_coordinates(legal_addresses)

    edges_list = get_distances(legal_addresses, coordinates_list)

    data = get_min_hamilton_cycle(edges_list)

    global route_id
    route_id += 1
    data["id"] = route_id
    database[route_id] = data
    msg = "SUCCESS: The shortest path has been successfully found"

    return {"message": msg, "shortest_path": database[route_id]}


@router.delete("/{route_id}/", description="Удалить маршрут")
async def delete_route(route_id: int):
    del database[route_id]
    return list(database.values())


@router.get("/{route_id}/", description="Получить маршрут по идентификатору")
async def get_route(route_id: int):
    return database[route_id]


@router.put("/{route_id}/", description="Изменить маршрут")
async def update_route(route_id: int, legal_addresses: List[LegalAddress]):
    address_list = get_coordinates(legal_addresses)

    edges_list = get_distances(legal_addresses, address_list)

    database[route_id] = get_min_hamilton_cycle(edges_list)
    msg = "SUCCESS: The shortest path has been successfully found"

    return {"message": msg, "shortest_path": database[route_id]}


# @router.patch("/{route_id}/")
# async def update_route(route_id: int, legal_addresses: List[LegalAddress]):
#     address_list = get_coordinates(legal_addresses)
#
#     data = get_distances(legal_addresses, address_list)
#
#     graph = HamiltonianGraph(data)
#     msg, data = graph.find_hamiltonian_cycle()
#     database[route_id] = data
#     return {"message": msg, "shortest_path": database[route_id]}
