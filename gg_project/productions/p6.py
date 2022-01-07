""" Implementation of production number 6
"""
import dataclasses
from itertools import combinations

import networkx as nx

from gg_project.productions import Production
from gg_project.productions.utils import Node, graph_id_sequence
from gg_project.vertex_params import VertexParams, VertexType


class Production6(Production):
    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        # FIXME: add later
        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
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
