from typing import List, Tuple

from requests import request

from api_v1.routes.schemas import LegalAddress, Geocoordinates


def get_coordinates(legal_addresses: List[LegalAddress]) -> List[Geocoordinates]:
    coordinates_list = []
    for legal_address in legal_addresses:
        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=legal_address.model_dump(),
        )
        coordinates_list.append(response.json().get("coordinates"))

    return coordinates_list


def get_distances(
    legal_addresses: List[LegalAddress], coordinates_list: List[Geocoordinates]
) -> List[Tuple[str, str, int]]:
    edges_list = []

    for i in range(0, len(coordinates_list)):
        for j in range(i + 1, len(coordinates_list)):
            response = request(
                method="POST",
                url="http://localhost:8002/api/v1/distance_matrix/",
                json={
                    "source": {**coordinates_list[i]},
                    "destination": {**coordinates_list[j]},
                },
            )
            duration = response.json().get("duration")
            edge = (
                f"{legal_addresses[i]}",
                f"{legal_addresses[j]}",
                duration,
            )
            edges_list.append(edge)

            edge = (
                f"{legal_addresses[j]}",
                f"{legal_addresses[i]}",
                duration,
            )
            edges_list.append(edge)

    return edges_list
