from typing import List, Dict, Type

from requests import request

from api_v1.routes.schemas import Geocoordinates
from app.models import model_dump, Order
from configs.settings import Category
from utils.graph import EdgesList


def get_coordinates(
        orders: List[Type[Order]],
) -> Dict[int, Geocoordinates]:
    coordinates_dict = {}
    for order in orders:
        address_dict = model_dump(order.address)
        address_dict.pop("id")

        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=address_dict,
        )
        coordinates_dict[order.id] = response.json().get("coordinates")

    return coordinates_dict


def get_distances(coordinates_dict: Dict[int, Geocoordinates], category: Category) -> EdgesList:
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

            durations = response.json().get("duration")
            transport, duration = "auto", durations.pop("auto")

            if category == Category.lightweight:
                transport, duration = min(durations.items(), key=lambda item: item[1])

            if all([d == duration for d in durations.values()]):
                transport = "pd"

            edges_list.add_edge(addr1, addr2, duration, transport)

            edges_list.add_edge(addr2, addr1, duration, transport)

    return edges_list
