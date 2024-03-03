from typing import List, Dict

from requests import request

from api_v1.routes.schemas import LegalAddress, Geocoordinates
from utils.graph import EdgesList


def get_coordinates(
    legal_addresses: List[LegalAddress],
) -> Dict[LegalAddress, Geocoordinates]:
    coordinates_dict = {}
    for legal_address in legal_addresses:
        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=legal_address.model_dump(),
        )
        coordinates_dict[legal_address] = response.json().get("coordinates")

    return coordinates_dict


def get_distances(
    coordinates_dict: Dict[LegalAddress, Geocoordinates]
) -> EdgesList:
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
