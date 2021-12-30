""" Implementation of production number 3
"""

import networkx as nx
from gg_project.vertex_params import VertexParams, VertexType

from . import Production
from .utils import all_neighbors_of_type

import itertools


def _get_exterior_neighbors(graph, node_id):
    return [
        n_id for n_id in graph.neighbors(node_id)
        if VertexParams(**graph.nodes[n_id]).vertex_type == VertexType.EXTERIOR
    ]


def _get_common_exterior_neighbors(graph, a, b):
    a_ne = set(_get_exterior_neighbors(graph, a))
    b_ne = set(_get_exterior_neighbors(graph, b))

    return a_ne & b_ne


def _has_external_common_neighbor(graph, a, b):
    neighbors = _get_common_exterior_neighbors(graph, a, b)
    return len(neighbors) >= 1


def _check_if_correct(graph: nx.Graph, x1, x2, x3):
    return (
            graph.has_edge(x1, x2)
            and graph.has_edge(x2, x3)
            and not graph.has_edge(x1, x3)
            and _has_external_common_neighbor(graph, x1, x3)
    )


def _find_correct_graph_order(graph, node_id):
    neighbors_ids = graph.neighbors(node_id)

    if len(neighbors_ids) == 3:
        for (a, b, c) in itertools.permutations([neighbors_ids[0], neighbors_ids[1], neighbors_ids[2]]):
            if _check_if_correct(graph, a, b, c):
                d = next(iter(_get_common_exterior_neighbors(graph, b, c)))  # TODO: yield moreeee
                return a, b, c, d

    return None


class Production3(Production):

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph):
        for node_id, params in graph.nodes.items():
            if (
                    VertexParams(**params).vertex_type == VertexType.INTERIOR
                    and all_neighbors_of_type(graph, node_id, VertexType.EXTERIOR)
            ):
                order = _find_correct_graph_order(graph, node_id)
                if order is not None:
                    a, b, c, d = order
                    return graph.subgraph([node_id, a, b, c, d])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        new_graph = graph.copy()
        assert len(subgraph.nodes) == 5

        interior_node_id = None
        for node_id, params in graph.nodes.items():
            if (VertexParams(**params)).vertex_type == VertexType.INTERIOR:
                interior_node_id = node_id

        assert interior_node_id is not None

        a, b, c, d = _find_correct_graph_order(graph, interior_node_id)

        new_graph.nodes[interior_node_id]["vertex_type"] = VertexType.INTERIOR_USED

        # TODO: implement nodes adding

        return new_graph
