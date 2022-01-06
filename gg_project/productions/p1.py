""" Implementation of production number 1

Authors:
Mirosław Błazej
Grzegorz Wcisło
Karol Szuster
"""

from typing import Iterator

import networkx as nx

from gg_project.vertex_params import VertexParams, VertexType

from . import Production


class Production1(Production):
    """Implementation of first production from documentation.

    This production takes start vertex from a graph and builds a single element.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> Iterator[nx.Graph]:
        for node_id, params in graph.nodes.items():
            if VertexParams(**params).vertex_type == VertexType.START:
                yield graph.subgraph([node_id])

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        new_graph = graph.copy()
        assert len(subgraph.nodes) == 1

        start_node_id, start_node_data = next(iter(subgraph.nodes.items()))

        vdata = VertexParams(**start_node_data)
        new_graph.nodes[start_node_id]["vertex_type"] = vdata

        return new_graph
