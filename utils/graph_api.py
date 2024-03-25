from utils.graph import HamiltonianGraph, Status, EdgesList


def get_min_hamiltonian_cycle(edges_list: EdgesList) -> dict:
    edges_list.sort()

    graph = HamiltonianGraph()
    min_duration = edges_list.sum()
    total_data = {}

    for edge in edges_list:
        graph.add_edge(edge.node_from, edge.node_to, edge.weight)
        status, data = graph.get_hamiltonian_cycle()

        if status != Status.OK:
            continue

        if min_duration > data["total_duration"]:
            min_duration = data["total_duration"]
            total_data = data

    return total_data
