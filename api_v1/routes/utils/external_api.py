import dataclasses
from typing import List, Dict, Type

from requests import request

from api_v1.routes.schemas import Geocoordinates
from app.models import Address, model_dump
from utils.graph import EdgesList


def get_coordinates(
    legal_addresses: List[Type[Address]],
) -> Dict[int, Geocoordinates]:
    coordinates_dict = {}
    for legal_address in legal_addresses:
        address_dict = model_dump(legal_address)
        address_id = address_dict.pop("id")

        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=address_dict,
        )
        coordinates_dict[address_id] = response.json().get("coordinates")

    return coordinates_dict


def get_distances(coordinates_dict: Dict[int, Geocoordinates]) -> EdgesList:
    edges_list = EdgesList()
    passed_addr = set()
    for addr1, coord1 in coordinates_dict.items():
        passed_addr.add(addr1)
        for addr2, coord2 in coordinates_dict.items():
            if addr2 in passed_addr:
                continue

            response = request(
                method="POST",
                url="http://localhost:8002/api/v1/distance_matrix/",
                json={
                    "source": {**coord1},
                    "destination": {**coord2},
                },
            )
            duration: int = response.json().get("duration")

            edges_list.add_edge(addr1, addr2, duration)

            edges_list.add_edge(addr2, addr1, duration)

    return edges_list
