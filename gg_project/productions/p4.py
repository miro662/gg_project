""" Implementation of production number 6
"""
import dataclasses
import itertools
from typing import Tuple, Sequence, List

import networkx as nx

from . import Production
from .utils import Node, graph_id_sequence, check_if_all_neighbors_of_type_and_level, \
    get_all_neighbors_same_level, get_params_with_lower_level
from gg_project.vertex_params import VertexParams, VertexType
from .p3 import _get_common_exterior_neighbors, _get_neighbour_with_correct_position


def _get_position_between_nodes(nodes: List[VertexParams]) -> Tuple[float, float]:
    return (
        sum(map(lambda node: node.position[0], nodes)) / len(nodes),
        sum(map(lambda node: node.position[1], nodes)) / len(nodes)
    )


def _find_mid_vertices(graph: nx.Graph, a: int, b: int, c: int) -> Tuple[int, int] | None:
    ab_neighbors = _get_common_exterior_neighbors(graph, a, b)
    ac_neighbors = _get_common_exterior_neighbors(graph, a, c)

    a_vertex = VertexParams(**graph.nodes[a])
    b_vertex = VertexParams(**graph.nodes[b])
    c_vertex = VertexParams(**graph.nodes[c])

    ab_position = _get_position_between_nodes([a_vertex, b_vertex])
    ac_position = _get_position_between_nodes([a_vertex, c_vertex])

    ab = _get_neighbour_with_correct_position(graph, ab_neighbors, ab_position)
    ac = _get_neighbour_with_correct_position(graph, ac_neighbors, ac_position)

    if ab is not None and ac is not None and graph.has_edge(b, c) and not graph.has_edge(a, b) \
            and not graph.has_edge(a, c):
        return ab, ac
    else:
        return None


def _find_correct_subgraph(graph: nx.Graph, node_id: int) -> Tuple[int, int, int, int, int] | None:
    neighbors_ids = get_all_neighbors_same_level(graph, node_id)

    if len(neighbors_ids) == 3:
        for (a, b, c) in itertools.permutations([neighbors_ids[0], neighbors_ids[1], neighbors_ids[2]]):
            mid_vertices = _find_mid_vertices(graph, a, b, c)
            if mid_vertices is not None:
                ab, ac = mid_vertices
                return a, b, c, ab, ac

    return None


def _find_internal_node(graph: nx.Graph) -> Node | None:
    for node_id, params in graph.nodes.items():
        vertex_params = VertexParams(**params)
        if vertex_params.vertex_type == VertexType.INTERIOR:
            return Node(node_id, vertex_params)
    return None


def _create_interior_node(a: Node, b: Node, c: Node, level: int, node_id: int) -> Node:
    return Node(
        node_id, VertexParams(
            vertex_type=VertexType.INTERIOR,
            position=_get_position_between_nodes([a.params, b.params, c.params]),
            level=level
        )
    )


def _create_edges(
        used_interior_node: Node,
        interior_node_a: Node,
        interior_node_c: Node,
        interior_node_cb: Node,
        exterior_node_a: Node,
        exterior_node_b: Node,
        exterior_node_c: Node,
        exterior_node_ab: Node,
        exterior_node_ac: Node
) -> Sequence[tuple[int, int]]:
    return [
        (used_interior_node.id, interior_node_a.id),
        (used_interior_node.id, interior_node_cb.id),

        (exterior_node_a.id, exterior_node_ac.id),
        (exterior_node_a.id, exterior_node_ab.id),
        (exterior_node_ab.id, exterior_node_ac.id),
        (exterior_node_ac.id, exterior_node_c.id),
        (exterior_node_ab.id, exterior_node_b.id),
        (exterior_node_ab.id, exterior_node_c.id),
        (exterior_node_b.id, exterior_node_c.id),

        (interior_node_a.id, exterior_node_a.id),
        (interior_node_a.id, exterior_node_ab.id),
        (interior_node_a.id, exterior_node_ac.id),

        (interior_node_c.id, exterior_node_c.id),
        (interior_node_c.id, exterior_node_ac.id),
        (interior_node_c.id, exterior_node_ab.id),

        (interior_node_cb.id, exterior_node_c.id),
        (interior_node_cb.id, exterior_node_b.id),
        (interior_node_cb.id, exterior_node_ab.id)
    ]


class Production4(Production):

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        for node_id, params in graph.nodes.items():
            if (
                    VertexParams(**params).vertex_type == VertexType.INTERIOR
                    and check_if_all_neighbors_of_type_and_level(graph, node_id, VertexType.EXTERIOR)
            ):
                correct_subgraph = _find_correct_subgraph(graph, node_id)
                if correct_subgraph is not None:
                    a, b, c, ab, ac = correct_subgraph
                    return graph.subgraph([node_id, a, b, c, ab, ac])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        next_id_val_fun = graph_id_sequence(graph)

        graph_copy = graph.copy()
        if len(subgraph.nodes) == 6:
            interior_node = _find_internal_node(subgraph)
            if interior_node is not None:
                a, b, c, ab, ac = _find_correct_subgraph(subgraph, interior_node.id)
                a_node = Node(a, VertexParams(**graph.nodes[a]))
                b_node = Node(b, VertexParams(**graph.nodes[b]))
                c_node = Node(c, VertexParams(**graph.nodes[c]))
                ab_node = Node(ab, VertexParams(**graph.nodes[ab]))
                ac_node = Node(ac, VertexParams(**graph.nodes[ac]))

                used_interior_node = Node(
                    interior_node.id,
                    dataclasses.replace(interior_node.params, vertex_type=VertexType.INTERIOR_USED)
                )
                interior_node_a = _create_interior_node(a_node, ab_node, ac_node, interior_node.params.level + 1,
                                                        next_id_val_fun())
                interior_node_c = _create_interior_node(ab_node, ac_node, c_node, interior_node.params.level + 1,
                                                        next_id_val_fun())
                interior_node_cb = _create_interior_node(ac_node, c_node, b_node, interior_node.params.level + 1,
                                                         next_id_val_fun())
                exterior_nodes = list(map(
                    lambda params: Node(next_id_val_fun(), params),
                    get_params_with_lower_level([a_node, b_node, c_node, ab_node, ac_node])
                ))

                new_nodes = [used_interior_node, interior_node_a, interior_node_c, interior_node_cb, *exterior_nodes]

                new_nodes_for_graph = map(lambda node: (node.id, dataclasses.asdict(node.params)), new_nodes)
                new_edges = _create_edges(
                    used_interior_node,
                    interior_node_a,
                    interior_node_c,
                    interior_node_cb,
                    *exterior_nodes
                )

                graph_copy.add_nodes_from(new_nodes_for_graph)
                graph_copy.add_edges_from(new_edges)
                return graph_copy

        return None
