from typing import List
from fastapi import APIRouter
from requests import request

from api_v1.routes.schemas import LegalAddress
from api_v1.routes.utils.graph import HamiltonianGraph
from api_v1.routes.utils.subrequests import get_coordinates, get_distances

router = APIRouter(tags=["ShortestPath"], prefix="/api/v1/shortest_path/routes")

route_id: int = 1
database: dict = {}


@router.get("/")
async def get_routes():
    return database


@router.post("/")
async def get_shortest_path(legal_addresses: List[LegalAddress]):
    address_list = await get_coordinates(legal_addresses)

    data = await get_distances(legal_addresses, address_list)

    graph = HamiltonianGraph(data)
    msg, data = graph.find_hamiltonian_cycle()
    global route_id
    database[route_id] = data
    route_id += 1
    return {"message": msg, "shortest_path": database[route_id - 1]}


@router.delete("/{route_id}/")
async def delete_route(route_id: int):
    del database[route_id]
    return database


@router.get("/{route_id}/")
async def get_route(route_id: int):
    return database[route_id]


@router.patch("/{route_id}/")
async def update_route(route_id: int, legal_addresses: List[LegalAddress]):
    address_list = await get_coordinates(legal_addresses)

    data = await get_distances(legal_addresses, address_list)

    graph = HamiltonianGraph(data)
    msg, data = graph.find_hamiltonian_cycle()
    database[route_id] = data
    return {"message": msg, "shortest_path": database[route_id]}


# @router.put("/{route_id}/")
# async def update_route(route_id: int, legal_addresses: List[LegalAddress]):
#     address_list = await get_coordinates(legal_addresses)
#
#     data = await get_distances(legal_addresses, address_list)
#
#     graph = HamiltonianGraph(data)
#     msg, data = graph.find_hamiltonian_cycle()
#     database[route_id] = data
#     return {"message": msg, "shortest_path": database[route_id]}
