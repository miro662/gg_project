""" Implementation of production number 1

Authors:
Mirosław Błazej
Grzegorz Wcisło
Karol Szuster
"""

import networkx as nx
from gg_project.vertex_params import VertexParams, VertexType

from . import Production


class Production1(Production):
    """Implementation of first production from documentation.

    This production takes start vertex from a graph and builds a single element.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        for node_id, params in graph.nodes.items():
            if VertexParams(**params).vertex_type == VertexType.START:
                return graph.subgraph([node_id])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        new_graph = graph.copy()
        assert len(subgraph.nodes) == 1

        start_node_id, _ = next(iter(subgraph.nodes.items()))
        new_graph.nodes[start_node_id]["vertex_type"] = VertexType.START_USED

        return new_graph
