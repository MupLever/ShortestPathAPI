from math import inf

from typing import List, Tuple

from api_v1.routes.schemas import LegalAddress
from utils.graph import HamiltonianGraph, Status


def get_min_hamiltonian_cycle(
    edges_list: List[Tuple[LegalAddress, LegalAddress, int]]
) -> dict:
    edges_list.sort(key=lambda edge: edge[2])

    graph = HamiltonianGraph()
    min_duration = inf
    total_data = {}

    for from_, to_, weight in edges_list:
        graph.add_edge(from_, to_, weight)
        status, data = graph.get_hamiltonian_cycle()

        if status != Status.OK:
            continue

        if min_duration > data["total_duration"]:
            min_duration = data["total_duration"]
            total_data = data

    return total_data
