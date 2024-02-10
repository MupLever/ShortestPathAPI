from typing import List
from fastapi import APIRouter
from requests import request

from api_v1.routes.schemas import LegalAddress
from utils.graph import HamiltonianGraph

router = APIRouter(tags=["ShortestPath"], prefix="/api/v1/shortest_path/routes")


@router.get("/")
async def get_routes():
    pass


@router.get("/{route_id}/")
async def get_route(route_id: int):
    pass


@router.patch("/{route_id}/")
async def update_route(route_id: int):
    pass


@router.delete("/{route_id}/")
async def delete_route(route_id: int):
    pass


@router.post("/")
async def get_shortest_path(legal_addresses: List[LegalAddress]):
    address_list = []
    for legal_address in legal_addresses:
        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=legal_address.model_dump(),
        )
        address_list.append(response.json().get("coordinates"))

    data = []

    for i in range(0, len(address_list)):
        for j in range(i + 1, len(address_list)):
            json_body = {
                "first_address": {
                    "latitude": address_list[i]["lat"],
                    "longitude": address_list[i]["lng"],
                },
                "second_address": {
                    "latitude": address_list[j]["lat"],
                    "longitude": address_list[j]["lng"],
                },
            }
            response = request(
                method="POST",
                url="http://localhost:8002/api/v1/distance_matrix/",
                json=json_body,
            )
            distance = int(response.json().get("distance"))
            edge = (
                f"{legal_addresses[i]}",
                f"{legal_addresses[j]}",
                distance,
            )
            data.append(edge)

            edge = (
                f"{legal_addresses[j]}",
                f"{legal_addresses[i]}",
                distance,
            )
            data.append(edge)

    graph = HamiltonianGraph(data)
    msg, data = graph.find_hamiltonian_cycle()
    return {"message": msg, "shortest_path": data}
