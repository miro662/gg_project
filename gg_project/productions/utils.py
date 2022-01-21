import collections
import dataclasses
from typing import List, Sequence, Callable

import networkx as nx

from gg_project.vertex_params import VertexParams, VertexType

NodeId = int
Node = collections.namedtuple("Node", ["id", "params"])


def get_all_neighbors_same_level(graph: nx.Graph, node_id: int) -> List[int]:
    node_level = VertexParams(**graph.nodes[node_id]).level
    neighbors = [
        neighbor_id
        for neighbor_id in graph.neighbors(node_id)
        if VertexParams(**graph.nodes[neighbor_id]).level == node_level
    ]
    return neighbors


def check_if_all_neighbors_of_type_and_level(
        graph: nx.Graph, node_id: int, vertex_type: VertexType
) -> bool:
    neighbors = [
        VertexParams(**graph.nodes[neighbor_id]).vertex_type
        for neighbor_id in get_all_neighbors_same_level(graph, node_id)
    ]

    return all(neighbor_type == vertex_type for neighbor_type in neighbors)


def move_down_node(params: VertexParams) -> VertexParams:
    return dataclasses.replace(params, level=params.level + 1)


def get_params_with_lower_level(nodes: Sequence[Node]) -> Sequence[VertexParams]:
    return list(map(lambda node: move_down_node(node.params), nodes))


def graph_id_sequence(graph: nx.Graph) -> Callable[[], NodeId]:
    next_id = max(graph.nodes) + 1

    def internal():
        nonlocal next_id
        rv = next_id
        next_id += 1
        return rv

    return internal
