# pylint: disable = invalid-name, too-many-locals, fixme

import collections
import dataclasses
import itertools
from itertools import combinations

import networkx as nx

from gg_project.productions import Production
from gg_project.vertex_params import VertexType, VertexParams

Node = collections.namedtuple("Node", ["id", "params"])


class Production7(Production):

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        isomorphic_graph = nx.Graph()

        isomorphic_graph.add_nodes_from(
            [
                (2, mk_vertex(VertexType.EXTERIOR)),
                (3, mk_vertex(VertexType.EXTERIOR)),

                (5, mk_vertex(VertexType.INTERIOR_USED)),
                (6, mk_vertex(VertexType.INTERIOR_USED)),

                (7, mk_vertex(VertexType.EXTERIOR)),
                (8, mk_vertex(VertexType.EXTERIOR)),
                (9, mk_vertex(VertexType.EXTERIOR)),
                (10, mk_vertex(VertexType.EXTERIOR)),

                (11, mk_vertex(VertexType.INTERIOR)),
                (12, mk_vertex(VertexType.INTERIOR)),

                (14, mk_vertex(VertexType.EXTERIOR)),
                (15, mk_vertex(VertexType.EXTERIOR)),
                (16, mk_vertex(VertexType.EXTERIOR)),

                (17, mk_vertex(VertexType.INTERIOR)),
                (18, mk_vertex(VertexType.INTERIOR)),
            ]
        )

        isomorphic_graph.add_edges_from(
            [
                (2, 3),
                (2, 5),
                (3, 5),
                (2, 6),
                (3, 6),
                (7, 8),
                (7, 9),
                (7, 10),
                (8, 10),
                (9, 10),
                (5, 11),
                (5, 12),
                (7, 11),
                (7, 12),
                (8, 11),
                (9, 12),
                (10, 11),
                (10, 12),
                (6, 17),
                (8, 15),
                (14, 15),
                (16, 17),
                (14, 17),
                (15, 17),
                (16, 14),
                (16, 8),
                (16, 18),
                (8, 18),
                (15, 18),
                (6, 18),
                (16, 15)
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
                if nx.is_isomorphic(subgraph, isomorphic_graph, node_match=are_types_equal):
                    nodes: list[Node] = list(
                        map(
                            lambda node: Node(node[0], VertexParams(**node[1])),
                            subgraph.nodes.items(),
                        ),
                    )

                    exterior_nodes: list[Node] = list(
                        filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
                    )
                    if len(list(get_duplicates_with_label(exterior_nodes))) == 2:
                        return subgraph

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        if subgraph is None:
            raise ValueError("Subgraph is not isomorphic to left side")

        new_graph = graph.copy()

        nodes: list[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                new_graph.nodes.items(),
            ),
        )

        max_node_id = max(node.id for node in nodes)

        exterior_nodes: list[Node] = list(
            filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
        )

        for E2s in get_duplicates_with_label(exterior_nodes):
            for E2L, E2R in combinations(E2s, 2):
                for E1 in get_common_neighbors_of_type(new_graph, nodes, E2L, E2R, VertexType.EXTERIOR):
                    for E3L in get_neighbors_of_type(new_graph, nodes, E2L, VertexType.EXTERIOR):
                        if E3L is not E1 and is_node_between(E1, E2L, E3L):
                            for E3R in get_duplicates_of(nodes, E3L):
                                if E3R is not E1 and is_node_between(E1, E2R, E3R):
                                    new_graph = merge_two_nodes(new_graph, E2L, E2R, max_node_id + 1)
                                    new_graph = merge_two_nodes(new_graph, E3L, E3R, max_node_id + 2)
                                    return new_graph


def get_duplicates_with_label(nodes: list[Node]):
    result = dict()
    for node in nodes:
        key = (node.params.position, node.params.level)
        if key in result:
            result[key].append(node)
        else:
            result[key] = [node]

    for value in result.values():
        if value.__len__() >= 2:
            yield value


def get_duplicates_of(nodes: list[Node], node: Node):
    return [n for n in nodes if n.params == node.params and n.id != node.id]


def find_node(node_id: int, nodes: list[Node]) -> Node:
    for node in nodes:
        if node.id == node_id:
            return node


def get_common_neighbors_of_type(graph: nx.Graph, nodes: list[Node], node1: Node, node2: Node, vertex_type: VertexType):
    for node in get_neighbors_of_type(graph, nodes, node1, vertex_type):
        if node in get_neighbors_of_type(graph, nodes, node2, vertex_type):
            yield node


def get_neighbors_of_type(graph: nx.Graph, nodes: list[Node], node: Node, vertex_type: VertexType) -> list[Node]:
    abc = [
        neighbor
        for neighbor in graph.neighbors(node.id)
        if graph.nodes[neighbor]["vertex_type"] == vertex_type
    ]

    return list(map(lambda neighbor: find_node(neighbor, nodes), abc))


def is_node_between(E1: Node, E2: Node, E3: Node) -> bool:
    return E2.params.position[0] == (E1.params.position[0] + E3.params.position[0]) / 2 \
           and E2.params.position[1] == (E1.params.position[1] + E3.params.position[1]) / 2


def merge_two_nodes(graph: nx.Graph, node_1: Node, node_2: Node, new_id: int):
    neighbors = set(graph.neighbors(node_1.id)) | set(graph.neighbors(node_2.id)) - {node_1.id, node_2.id}
    graph.add_nodes_from([(new_id, dataclasses.asdict(node_1.params))])
    graph.remove_node(node_1.id)
    graph.remove_node(node_2.id)
    graph.add_edges_from([(n, new_id) for n in neighbors])
    return graph


def mk_vertex(t):
    return dataclasses.asdict(VertexParams(vertex_type=t, position=(0.0, 0.0), level=0))


def are_types_equal(node1, node2) -> bool:
    return VertexParams(**node1).vertex_type == VertexParams(**node2).vertex_type
