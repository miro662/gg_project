""" Implementation of production number 5

Authors:
Jacek Skierski
Bartosz Drzewicki
"""

import dataclasses
from typing import List, Tuple, Optional, Sequence

import networkx as nx
from gg_project.vertex_params import VertexParams, VertexType, check_if_positions_equal

from . import Production
from .utils import check_if_all_neighbors_of_type_and_level, get_all_neighbors_same_level, \
    Node, graph_id_sequence, get_params_with_lower_level

import itertools


def _find_correct_graph_order(graph: nx.Graph, node_id: int) -> Optional[Tuple[int, int, int, int, int, int]]:
    neighbors_ids = get_all_neighbors_same_level(graph, node_id)

    if len(neighbors_ids) == 3:
        a = neighbors_ids[0]
        b = neighbors_ids[1]
        c = neighbors_ids[2]
        # for (a, b, c) in itertools.permutations([neighbors_ids[0], neighbors_ids[1], neighbors_ids[2]]):
        correct, d, e, f = _check_if_correct(graph, a, b, c)
        if correct:
            return a, b, c, d, e, f

    return None


def _check_if_correct(graph: nx.Graph, x1: int, x2: int, x3: int):
    external_neighbors13 = _get_common_exterior_neighbors(graph, x1, x3)
    external_neighbors12 = _get_common_exterior_neighbors(graph, x1, x2)
    external_neighbors23 = _get_common_exterior_neighbors(graph, x2, x3)

    x1_vertex = VertexParams(**graph.nodes[x1])
    x2_vertex = VertexParams(**graph.nodes[x2])
    x3_vertex = VertexParams(**graph.nodes[x3])

    x4_position = (
        (x1_vertex.position[0] + x3_vertex.position[0]) / 2,
        (x1_vertex.position[1] + x3_vertex.position[1]) / 2
    )

    x5_position = (
        (x2_vertex.position[0] + x3_vertex.position[0]) / 2,
        (x2_vertex.position[1] + x3_vertex.position[1]) / 2
    )

    x6_position = (
        (x1_vertex.position[0] + x2_vertex.position[0]) / 2,
        (x1_vertex.position[1] + x2_vertex.position[1]) / 2
    )

    x4 = _get_neighbour_with_correct_position(graph, external_neighbors13, x4_position)
    x5 = _get_neighbour_with_correct_position(graph, external_neighbors23, x5_position)
    x6 = _get_neighbour_with_correct_position(graph, external_neighbors12, x6_position)

    x4_condition = not graph.has_edge(x1, x2) and not graph.has_edge(x2, x3) and not graph.has_edge(x1, x3)
    x5_condition = x5 is not None and x6 is not None and x4 is not None

    return (x4_condition and x5_condition), x4, x5, x6


def _create_edge(node_a: Node, node_b: Node) -> Tuple[int, int]:
    return node_a.id, node_b.id


def _create_edges(
        used_interior_node: Node,
        interior_node_0: Node,
        interior_node_1: Node,
        interior_node_2: Node,
        interior_node_3: Node,
        exterior_node_a: Node,
        exterior_node_b: Node,
        exterior_node_c: Node,
        exterior_node_d: Node,
        exterior_node_e: Node,
        exterior_node_f: Node
) -> Sequence[tuple[int, int]]:
    return [
        _create_edge(used_interior_node, interior_node_0),
        _create_edge(used_interior_node, interior_node_1),
        _create_edge(used_interior_node, interior_node_2),
        _create_edge(used_interior_node, interior_node_3),

        _create_edge(exterior_node_a, exterior_node_f),
        _create_edge(exterior_node_a, exterior_node_d),
        _create_edge(exterior_node_a, interior_node_0),

        _create_edge(exterior_node_b, exterior_node_f),
        _create_edge(exterior_node_b, exterior_node_d),
        _create_edge(exterior_node_b, exterior_node_e),
        _create_edge(exterior_node_b, interior_node_1),
        _create_edge(exterior_node_b, interior_node_2),

        _create_edge(exterior_node_c, exterior_node_d),
        _create_edge(exterior_node_c, exterior_node_e),
        _create_edge(exterior_node_c, interior_node_3),

        _create_edge(exterior_node_d, interior_node_0),
        _create_edge(exterior_node_d, interior_node_1),
        _create_edge(exterior_node_d, interior_node_2),
        _create_edge(exterior_node_d, interior_node_3),
        _create_edge(exterior_node_d, exterior_node_f),
        _create_edge(exterior_node_d, exterior_node_e),

        _create_edge(exterior_node_e, interior_node_2),
        _create_edge(exterior_node_e, interior_node_3),

        _create_edge(exterior_node_f, interior_node_0),
        _create_edge(exterior_node_f, interior_node_1)
    ]


def _get_neighbour_with_correct_position(
        graph,
        neighbors_ids: List[int],
        position: Tuple[float, float]) -> Optional[int]:
    for neighbor_id in neighbors_ids:
        vert = VertexParams(**graph.nodes[neighbor_id])

        if check_if_positions_equal(vert.position, position):
            return neighbor_id
    return None


def _get_common_exterior_neighbors(graph, a, b) -> List[int]:
    a_ne = set(_get_exterior_neighbors(graph, a))
    b_ne = set(_get_exterior_neighbors(graph, b))

    return list(a_ne & b_ne)


def _get_exterior_neighbors(graph, node_id):
    return [
        n_id for n_id in get_all_neighbors_same_level(graph, node_id)
        if VertexParams(**graph.nodes[n_id]).vertex_type == VertexType.EXTERIOR
    ]


def _get_node_from_id(graph: nx.Graph, node_id: int) -> Node:
    return Node(node_id, VertexParams(**graph.nodes[node_id]))


def _get_position_middle(
        pos1: Tuple[float, float],
        pos2: Tuple[float, float],
        pos3: Tuple[float, float]
) -> Tuple[float, float]:
    return (
        (pos1[0] + pos2[0] + pos3[0]) / 3,
        (pos1[1] + pos2[1] + pos3[1]) / 3,
    )


class Production5(Production):
    """Implementation of fifth production from documentation.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph):
        for node_id, params in graph.nodes.items():
            if (
                    VertexParams(**params).vertex_type == VertexType.INTERIOR
                    and check_if_all_neighbors_of_type_and_level(graph, node_id, VertexType.EXTERIOR)
            ):
                order = _find_correct_graph_order(graph, node_id)
                if order is not None:
                    a, b, c, d, e, f = order
                    return graph.subgraph([node_id, a, b, c, d, e, f])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        next_id_val_fun = graph_id_sequence(graph)

        new_graph = graph.copy()
        assert len(subgraph.nodes) == 7

        interior_node = None
        for node_id, params in subgraph.nodes.items():
            vertex_params = VertexParams(**params)
            if vertex_params.vertex_type == VertexType.INTERIOR:
                interior_node = Node(node_id, vertex_params)

        assert interior_node is not None

        current_level = interior_node.params.level

        a, b, c, d, e, f = _find_correct_graph_order(subgraph, interior_node.id)
        node_a = _get_node_from_id(graph, a)
        node_b = _get_node_from_id(graph, b)
        node_c = _get_node_from_id(graph, c)
        node_d = _get_node_from_id(graph, d)
        node_e = _get_node_from_id(graph, e)
        node_f = _get_node_from_id(graph, f)

        used_internal_node = Node(
            interior_node.id,
            dataclasses.replace(
                interior_node.params, vertex_type=VertexType.INTERIOR_USED
            ),
        )

        new_interior_0 = Node(
            next_id_val_fun(),
            VertexParams(
                vertex_type=VertexType.INTERIOR,
                position=_get_position_middle(
                    node_a.params.position,
                    node_f.params.position,
                    node_d.params.position
                ),
                level=current_level + 1
            )
        )

        new_interior_1 = Node(
            next_id_val_fun(),
            VertexParams(
                vertex_type=VertexType.INTERIOR,
                position=_get_position_middle(
                    node_f.params.position,
                    node_b.params.position,
                    node_d.params.position,
                ),
                level=current_level + 1
            )
        )

        new_interior_2 = Node(
            next_id_val_fun(),
            VertexParams(
                vertex_type=VertexType.INTERIOR,
                position=_get_position_middle(
                    node_b.params.position,
                    node_d.params.position,
                    node_e.params.position,
                ),
                level=current_level + 1
            )
        )

        new_interior_3 = Node(
            next_id_val_fun(),
            VertexParams(
                vertex_type=VertexType.INTERIOR,
                position=_get_position_middle(
                    node_d.params.position,
                    node_c.params.position,
                    node_e.params.position,
                ),
                level=current_level + 1
            )
        )

        new_exterior_nodes = list(
            map(
                lambda params: Node(next_id_val_fun(), params),
                get_params_with_lower_level([node_a, node_b, node_c, node_d, node_e, node_f]),
            )
        )

        new_level_nodes: list[Node] = [
            used_internal_node,
            new_interior_0,
            new_interior_1,
            new_interior_2,
            new_interior_3,
            *new_exterior_nodes
        ]
        new_level_raw_nodes = map(
            lambda node: (node.id, dataclasses.asdict(node.params)), new_level_nodes
        )

        edges = _create_edges(
            used_internal_node,
            new_interior_0,
            new_interior_1,
            new_interior_2,
            new_interior_3,
            *new_exterior_nodes
        )

        new_graph.add_nodes_from(new_level_raw_nodes)
        new_graph.add_edges_from(edges)

        return new_graph
