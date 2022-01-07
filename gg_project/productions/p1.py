""" Implementation of production number 1

Authors:
Mirosław Błazej
Grzegorz Wcisło
Karol Szuster
"""

from dataclasses import asdict

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

        last_node_id = len(graph.nodes)

        start_node_id, _ = next(iter(subgraph.nodes.items()))
        new_graph.nodes[start_node_id]["vertex_type"] = VertexType.START_USED

        nodes = [
            VertexParams(vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
            VertexParams(vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
            VertexParams(vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1),
            VertexParams(vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
            VertexParams(
                vertex_type=VertexType.INTERIOR, position=(0.25, 0.25), level=1
            ),
            VertexParams(
                vertex_type=VertexType.INTERIOR, position=(0.75, 0.75), level=1
            ),
        ]

        new_graph.add_nodes_from(
            (last_node_id + i, asdict(node)) for i, node in enumerate(nodes)
        )

        edges = [
            # start <-> interior
            (start_node_id, last_node_id + 4),
            (start_node_id, last_node_id + 5),
            # interior 1 <-> exterior
            (last_node_id + 0, last_node_id + 4),
            (last_node_id + 1, last_node_id + 4),
            (last_node_id + 2, last_node_id + 4),
            # interior 2 <-> exterior
            (last_node_id + 1, last_node_id + 5),
            (last_node_id + 2, last_node_id + 5),
            (last_node_id + 3, last_node_id + 5),
            # exterior
            (last_node_id + 0, last_node_id + 1),
            (last_node_id + 0, last_node_id + 2),
            (last_node_id + 1, last_node_id + 3),
            (last_node_id + 2, last_node_id + 3),
            (last_node_id + 1, last_node_id + 2),
        ]

        new_graph.add_edges_from(edges)

        return new_graph
