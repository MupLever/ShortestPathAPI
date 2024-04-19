from typing import Any

from utils.graph import HamiltonianGraph, Status, EdgesList


def get_min_hamiltonian_cycle(edges_list: EdgesList, start_value: Any = None) -> dict:
    edges_list.sort()

    graph = HamiltonianGraph()
    min_duration = edges_list.sum()
    total_data = {}

    for edge in edges_list:
        graph.add_edge(*edge.tuple)
        status, data = graph.get_hamiltonian_cycle(start_value=start_value)

        if status != Status.OK:
            continue

        if min_duration > data["total_duration"]:
            min_duration = data["total_duration"]
            total_data = data

    return total_data
