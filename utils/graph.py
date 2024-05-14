"""
The module allows you to create an arbitrary weighted graph,
has methods for traversing the graph in depth and width, a method
for searching for a Hamiltonian cycle
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Iterable, Tuple, Set, Iterator
from queue import Queue
from random import choice

from app.types import Transport


class Status(Enum):
    OK: int = 0
    ERROR: int = 1


class MatrixGraph:
    """"""

    def __init__(self) -> None:
        self.n_vertex = 0
        self.matrix = []
        self.graph = {}

    def add_or_get_node(self, value: Any) -> int:
        if value not in self.graph:
            self.n_vertex += 1
            for row in self.matrix:
                row.append(0)

            self.graph[value] = self.n_vertex - 1
            self.matrix.append([0 for _ in range(self.n_vertex)])

        return self.graph[value]

    def add_edge(self, value_from: Any, value_to: Any, weight: float) -> None:
        node_from = self.add_or_get_node(value_from)
        node_to = self.add_or_get_node(value_to)
        self.matrix[node_from][node_to] = weight

    def traverse(self) -> None:
        for row in self.matrix:
            print(row, end="\n")


class EdgesList:
    class Edge:
        def __init__(
            self, node_from: Any, node_to: Any, weight: int, transport: Transport
        ) -> None:
            self.node_from = node_from
            self.node_to = node_to
            self.weight = weight
            self.transport = transport

        def __radd__(self, other) -> int:
            return self.weight + other

        @property
        def tuple(self) -> tuple:
            return self.node_from, self.node_to, self.weight, self.transport

    def __init__(self) -> None:
        self.edges_list: list = []
        self._nodes = set()

    @property
    def n_vertex(self) -> int:
        return len(self._nodes)

    def __iter__(self) -> Iterator:
        return iter(self.edges_list)

    def add_edge(
        self, value_from: Any, value_to: Any, weight: int, transport: Transport
    ) -> None:
        self._nodes.update({value_from, value_to})

        edge = self.Edge(value_from, value_to, weight, transport)
        self.edges_list.append(edge)

    def sort(self, desc: bool = False) -> None:
        self.edges_list.sort(key=lambda edge: -edge.weight if desc else edge.weight)

    def sum(self) -> int:
        return sum(self.edges_list)

    def to_hamiltonian_graph(self) -> HamiltonianGraph:
        graph = HamiltonianGraph()
        for edge in self.edges_list:
            graph.add_edge(edge.node_from, edge.node_to, edge.weight, edge.transport)

        return graph


class HashTableGraph:
    """a directed graph class implemented through a dictionary"""

    class Node:
        """node class storing node value and incident edges"""

        def __init__(self, value: Any) -> None:
            self.value = value
            self.edges = set()
            self.parents = {}

        def __ne__(self, other) -> bool:
            if not isinstance(other, type(self)):
                return True

            return self.value != other.value

        def __eq__(self, other) -> bool:
            if not isinstance(other, type(self)):
                return False

            return self.value == other.value

        def __hash__(self) -> int:
            return hash(self.value)

        def __repr__(self) -> str:
            return f"{self.value}"

    class Edge:
        """edge class storing the incident node"""

        def __init__(self, incident_node, weight: int, transport: Transport) -> None:
            self.incident_node = incident_node
            self.weight = weight
            self.transport = transport

        def __lt__(self, other) -> bool:
            return self.weight < other.weight

        def __repr__(self) -> str:
            return f"<Edge: weight={self.weight}, incident_node={self.incident_node}>"

    def __init__(self) -> None:
        self.graph = {}
        self.n_vertex = 0

    def add_from_edges_list(self, edges_list: Iterable[Tuple[Any, Any, int]]) -> None:
        for from_, to_, weight, transport in edges_list:
            self.add_or_get_node(from_)
            self.add_or_get_node(to_)
            self.add_edge(from_, to_, weight, transport)

    def add_or_get_node(self, value: Any) -> Node:
        """adding and returning a node"""

        if value not in self.graph:
            self.graph[value] = self.Node(value)
            self.n_vertex += 1

        return self.graph[value]

    def add_edge(
        self, value_from: Any, value_to: Any, weight: int, transport: Transport
    ) -> None:
        node_from = self.add_or_get_node(value_from)
        node_to = self.add_or_get_node(value_to)

        edge = self.Edge(node_to, weight, transport)
        node_from.edges.add(edge)
        node_to.parents[node_from] = edge

    def delete_node(self, value: Any) -> None:
        raise NotImplementedError

    def delete_edge(self, value_from: Any, value_to: Any) -> None:
        if value_from not in self.graph:
            raise KeyError(
                f"the graph does not contain vertices with the value={value_from}"
            )

        if value_to not in self.graph:
            raise KeyError(
                f"the graph does not contain vertices with the value={value_to}"
            )

        node_from = self.graph[value_from]
        node_to = self.graph[value_to]

        edge = node_to.parents[node_from]
        node_from.edges.remove(edge)
        node_to.parents.pop(node_from)

    def traverse(self, *, how: str = "dfs") -> None:
        """
        wrapper for traversing all nodes of the graph.
        :param how: graph traversal algorithm, values: ``bfs``, ``dfs`` or ``rdfs``
        """
        how = how.lower()
        if how == "bfs":
            traverse_ = self._bfs
        elif how == "dfs":
            traverse_ = self._dfs_without_recur
        elif how == "rdfs":
            traverse_ = self._dfs_with_recur
        else:
            raise ValueError("invalid argument value")

        passed = set()
        for node in self.graph.values():
            if node not in passed:
                traverse_(node, passed)

    @staticmethod
    def _bfs(node: Node, passed: Set[Node]) -> None:
        """breadth-first traversal with queue"""

        queue = Queue()
        queue.put(node)
        while not queue.empty():
            node = queue.get()
            passed.add(node)
            print(node)
            for edge in node.edges:
                if edge.incident_node not in passed:
                    queue.put(edge.incident_node)
                    passed.add(edge.incident_node)

    @staticmethod
    def _dfs_without_recur(node: Node, passed: Set[Node]) -> None:
        """depth-first traversal without recursion"""

        stack = [node]
        while stack:
            node = stack[-1]
            if node not in passed:
                print(node)
                passed.add(node)
            has_children = False
            for edge in node.edges:
                if edge.incident_node not in passed:
                    stack.append(edge.incident_node)
                    has_children = True
                    break
            if not has_children:
                stack.pop()

    def _dfs_with_recur(self, node: Node, passed: Set[Node]) -> None:
        """depth-first traversal with recursion"""

        print(node.value)
        passed.add(node)
        for edge in node.edges:
            if edge.incident_node not in passed:
                self._dfs_with_recur(edge.incident_node, passed)


class HamiltonianGraph(HashTableGraph):
    def _ore_theorem(self) -> bool:
        """verifies Ore's theorem"""

        if self.n_vertex < 3:
            return False

        for node1 in self.graph.values():
            for node2 in self.graph.values():
                if (
                    node1 != node2
                    and node2 not in node1.parents
                    and node1 not in node2.parents
                    and len(node1.edges) + len(node2.edges) < self.n_vertex
                ):

                    return False

        return True

    @staticmethod
    def _get_edge_between(node, adjacent_node):
        """return weight between adjacent nodes"""

        if adjacent_node in node.parents:
            return node.parents[adjacent_node]

        if node in adjacent_node.parents:
            return adjacent_node.parents[node]

        return None

    @staticmethod
    def _get_nearest_not_passed_node(node, passed: set) -> Any:
        """returns the nearest unmarked node"""

        edges_to_not_passed_nodes = list(
            filter(lambda edge: edge.incident_node not in passed, node.edges)
        )

        if not edges_to_not_passed_nodes:
            return None

        edge_to_nearest_node = min(edges_to_not_passed_nodes)

        return edge_to_nearest_node.incident_node

    def get_hamiltonian_cycle(
        self, *, chain: bool = False, start_value: Any = None
    ) -> (int, dict):
        """finds a suboptimal Hamiltonian cycle"""

        data = {"path": [], "total_duration": 0}
        if not self._ore_theorem():
            return Status.ERROR, data

        if start_value is None:
            start_node = choice(list(self.graph.values()))
        elif start_value in self.graph:
            start_node = self.graph[start_value]
        else:
            raise KeyError(
                f"The graph doesn't contain vertices with this value={start_value}"
            )

        data["path"].append(
            {"node": start_node.value, "duration": 0, "transport": Transport.pd.value}
        )

        cur_node = start_node
        passed = {cur_node}

        while len(passed) < self.n_vertex:
            nearest_node = self._get_nearest_not_passed_node(cur_node, passed)
            if nearest_node is None:
                return Status.ERROR, {"path": [], "total_duration": 0}

            edge = self._get_edge_between(cur_node, nearest_node)
            if edge is None:
                return Status.ERROR, {"path": [], "total_duration": 0}

            data["path"].append(
                {
                    "node": nearest_node.value,
                    "duration": edge.weight,
                    "transport": edge.transport,
                }
            )
            data["total_duration"] += edge.weight
            passed.add(nearest_node)
            cur_node = nearest_node

        if not chain:
            edge = self._get_edge_between(start_node, cur_node)
            if edge is None:
                return Status.ERROR, {"path": [], "total_duration": 0}

            data["path"].append(
                {
                    "node": start_node.value,
                    "duration": edge.weight,
                    "transport": edge.transport,
                }
            )
            data["total_duration"] += edge.weight

        return Status.OK, data
