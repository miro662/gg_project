""" Implementation of production number 2

Authors:
Mirosław Błazej
Grzegorz Wcisło
Karol Szuster
"""

from contextlib import suppress
import networkx as nx
from gg_project.vertex_params import VertexParams, VertexType

from . import Production


def _all_neighbors_of_type(
    graph: nx.Graph, node_id: int, vertex_type: VertexType
) -> bool:
    neighbor_types = (
        VertexParams(**graph.nodes[neighbor_id]).vertex_type
        for neighbor_id in graph.neighbors(node_id)
    )
    return all(neighbor_type == vertex_type for neighbor_type in neighbor_types)


class Production2(Production):
    """Implementation of second production from documentation.

    This production takes an unbroken triangle tile from a graph and produces a new break.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        for node_id, params in graph.nodes.items():
            if (VertexParams(**params)).vertex_type != VertexType.INTERIOR:
                continue

            if not _all_neighbors_of_type(graph, node_id, VertexType.EXTERIOR):
                continue

            with suppress(nx.NetworkXNoCycle):
                nx.find_cycle(graph, graph.subgraph(graph.neighbors(node_id)))
                return graph.subgraph([node_id, *graph.neighbors(node_id)])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        raise NotImplementedError
