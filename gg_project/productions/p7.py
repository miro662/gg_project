# pylint: disable = invalid-name, too-many-locals, fixme

import collections
import dataclasses
from itertools import combinations

import networkx as nx

from gg_project.productions import Production
from gg_project.vertex_params import VertexType, VertexParams

Node = collections.namedtuple("Node", ["id", "params"])


class Production7(Production):
    """Implementation of second production from documentation.

    This production takes an unbroken triangle tile from a graph and produces a new break.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
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
                                    new_graph = merge_two_nodes(new_graph, E2L, E2R, max_node_id+1)
                                    new_graph = merge_two_nodes(new_graph, E3L, E3R, max_node_id+2)

                                    for a, _ in new_graph.nodes.items():
                                        print(str(a) + ',')
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
    return E2.params.position[0] == (E1.params.position[0] + E3.params.position[0]) / 2 and E2.params.position[1] == (E1.params.position[1] + E3.params.position[1]) / 2


def merge_two_nodes(graph: nx.Graph, node_1: Node, node_2: Node, new_id: int):
    neighbors = set(graph.neighbors(node_1.id)) | set(graph.neighbors(node_2.id)) - {node_1.id, node_2.id}
    graph.add_nodes_from([(new_id, dataclasses.asdict(node_1.params))])
    graph.remove_node(node_1.id)
    graph.remove_node(node_2.id)
    graph.add_edges_from([(n, new_id) for n in neighbors])
    return graph
