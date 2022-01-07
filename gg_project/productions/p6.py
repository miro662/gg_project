""" Implementation of production number 6
"""
import dataclasses
import itertools
from dataclasses import asdict
from itertools import combinations

import networkx as nx

from gg_project.productions import Production
from gg_project.productions.utils import Node, graph_id_sequence
from gg_project.vertex_params import VertexParams, VertexType


class Production6(Production):
    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        isomorphic_graph = nx.Graph()
        isomorphic_graph.add_nodes_from(
            [
                (1, _mk_vertex(VertexType.EXTERIOR)),
                (2, _mk_vertex(VertexType.EXTERIOR)),

                (3, _mk_vertex(VertexType.INTERIOR_USED)),
                (4, _mk_vertex(VertexType.INTERIOR_USED)),

                (5, _mk_vertex(VertexType.INTERIOR)),
                (6, _mk_vertex(VertexType.INTERIOR)),
                (7, _mk_vertex(VertexType.INTERIOR)),
                (8, _mk_vertex(VertexType.INTERIOR)),

                (9, _mk_vertex(VertexType.EXTERIOR)),
                (10, _mk_vertex(VertexType.EXTERIOR)),

                (11, _mk_vertex(VertexType.EXTERIOR)),
                (12, _mk_vertex(VertexType.EXTERIOR)),

                (13, _mk_vertex(VertexType.EXTERIOR)),
                (14, _mk_vertex(VertexType.EXTERIOR)),
            ]
        )

        isomorphic_graph.add_edges_from(
            [
                (1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 5),
                (3, 6), (4, 7), (4, 8), (9, 5), (10, 7), (11, 9),
                (12, 10), (12, 7), (12, 8), (13, 11), (11, 5), (11, 6),
                (13, 6), (14, 12), (14, 8)
            ]
        )

        node_diff = len(graph.nodes) - len(isomorphic_graph.nodes)

        if node_diff >= 0:
            all_connected_subgraphs = []

            for SG in (graph.subgraph(selected_nodes) for selected_nodes in
                       itertools.combinations(graph, len(isomorphic_graph))):
                if nx.is_connected(SG):
                    all_connected_subgraphs.append(SG)

            for subgraph in all_connected_subgraphs:
                if nx.is_isomorphic(subgraph, isomorphic_graph):
                    return subgraph

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        if cls.find_isomorphic_to_left_side(subgraph) is None:
            raise ValueError("Subgraph is not isomorphic to left side")

        next_id_val_fun = graph_id_sequence(graph)

        new_graph = graph.copy()

        nodes: list[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                subgraph.nodes.items(),
            ),
        )

        exterior_nodes: list[Node] = list(
            filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
        )

        for e_pairs in _get_duplicates_with_label(exterior_nodes):
            for e_left, e_right in combinations(e_pairs, 2):
                new_graph = _merge_two_nodes(new_graph, e_left, e_right, next_id_val_fun())

        return new_graph


def _get_duplicates_with_label(nodes: list[Node]):
    result = dict()
    for node in nodes:
        key = (node.params.position, node.params.level)
        if key in result:
            result[key].append(node)
        else:
            result[key] = [node]

    for value in result.values():
        if len(value) >= 2:
            yield value


def _merge_two_nodes(graph: nx.Graph, node_1: Node, node_2: Node, new_id: int):
    neighbors = set(graph.neighbors(node_1.id)) | set(graph.neighbors(node_2.id)) - {node_1.id, node_2.id}

    graph.add_nodes_from([(new_id, dataclasses.asdict(node_1.params))])
    graph.add_edges_from([(n, new_id) for n in neighbors])

    graph.remove_node(node_1.id)
    graph.remove_node(node_2.id)

    return graph


def _mk_vertex(t):
    return asdict(VertexParams(vertex_type=t, position=(0.0, 0.0), level=0))
