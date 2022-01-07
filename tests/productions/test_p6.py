import dataclasses

import networkx as nx
import pytest

from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import production6


def mk_vertex(t, pos, level):
    return dataclasses.asdict(VertexParams(vertex_type=t, position=pos, level=level))


def _are_nodes_equal(node1, node2) -> bool:
    return VertexParams(**node1) == VertexParams(**node2)


def _are_graphs_isomorphic(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    return nx.is_isomorphic(
        graph1,
        graph2,
        node_match=_are_nodes_equal
    )


@pytest.fixture
def correct_graph_for_left_side_p6():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),

            (3, mk_vertex(VertexType.INTERIOR_USED, (1 / 3, 1 / 3), 1)),
            (4, mk_vertex(VertexType.INTERIOR_USED, (2 / 3, 2 / 3), 1)),

            (5, mk_vertex(VertexType.INTERIOR, (1 / 4, 0.0), 2)),
            (6, mk_vertex(VertexType.INTERIOR, (1 / 4, 1.0), 2)),
            (7, mk_vertex(VertexType.INTERIOR, (3 / 4, 0.0), 2)),
            (8, mk_vertex(VertexType.INTERIOR, (3 / 4, 1.0), 2)),

            (9, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),

            (11, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),
            (12, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2)),
            (14, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2)),
        ]
    )

    graph.add_edges_from(
        [
            (1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 5),
            (3, 6), (4, 7), (4, 8), (9, 5), (10, 7), (11, 9),
            (12, 10), (12, 7), (12, 8), (13, 11), (11, 5), (11, 6),
            (13, 6), (14, 12), (14, 8)
        ]
    )

    return graph


@pytest.fixture
def correct_graph_for_p6_right_side():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),

            (3, mk_vertex(VertexType.INTERIOR_USED, (1 / 3, 1 / 3), 1)),
            (4, mk_vertex(VertexType.INTERIOR_USED, (2 / 3, 2 / 3), 1)),

            (5, mk_vertex(VertexType.INTERIOR, (1 / 4, 0.0), 2)),
            (6, mk_vertex(VertexType.INTERIOR, (1 / 4, 1.0), 2)),
            (7, mk_vertex(VertexType.INTERIOR, (3 / 4, 0.0), 2)),
            (8, mk_vertex(VertexType.INTERIOR, (3 / 4, 1.0), 2)),

            (15, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),

            (16, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (17, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2)),
        ]
    )

    graph.add_edges_from(
        [
            (1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 5), (3, 6), (4, 7), (4, 8),
            (5, 16), (5, 15),
            (6, 16,), (6, 17),
            (7, 15), (7, 16),
            (8, 16), (8, 17),
            (17, 16), (16, 15)
        ]
    )

    return graph


@pytest.fixture
def bigger_graph_for_p6_left_side():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (99, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),

            (3, mk_vertex(VertexType.INTERIOR_USED, (1 / 3, 1 / 3), 1)),
            (4, mk_vertex(VertexType.INTERIOR_USED, (2 / 3, 2 / 3), 1)),

            (5, mk_vertex(VertexType.INTERIOR, (1 / 4, 0.0), 2)),
            (6, mk_vertex(VertexType.INTERIOR, (1 / 4, 1.0), 2)),
            (7, mk_vertex(VertexType.INTERIOR, (3 / 4, 0.0), 2)),
            (8, mk_vertex(VertexType.INTERIOR, (3 / 4, 1.0), 2)),

            (9, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),

            (11, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),
            (12, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2)),
            (14, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2)),
        ]
    )

    graph.add_edges_from(
        [
            (99, 1), (99, 2), (99, 3),
            (1, 2), (0, 3), (1, 3), (2, 3),
            (0, 4), (1, 4), (2, 4), (3, 5),
            (3, 6), (4, 7), (4, 8), (9, 5),
            (10, 7), (11, 9), (11, 5), (11, 6),
            (12, 10), (12, 7), (12, 8), (13, 11),
            (13, 6), (14, 12), (14, 8)
        ]
    )

    return graph


@pytest.fixture
def bigger_graph_for_p6_right_side():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (99, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),

            (3, mk_vertex(VertexType.INTERIOR_USED, (1 / 3, 1 / 3), 1)),
            (4, mk_vertex(VertexType.INTERIOR_USED, (2 / 3, 2 / 3), 1)),

            (5, mk_vertex(VertexType.INTERIOR, (1 / 4, 0.0), 2)),
            (6, mk_vertex(VertexType.INTERIOR, (1 / 4, 1.0), 2)),
            (7, mk_vertex(VertexType.INTERIOR, (3 / 4, 0.0), 2)),
            (8, mk_vertex(VertexType.INTERIOR, (3 / 4, 1.0), 2)),

            (100, mk_vertex(VertexType.EXTERIOR, (0.5, 0.0), 2)),

            (101, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (102, mk_vertex(VertexType.EXTERIOR, (0.5, 1.0), 2))
        ]
    )

    graph.add_edges_from(
        [
            (1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 5), (3, 6), (4, 7), (4, 8),
            (5, 101), (5, 100),
            (6, 101), (6, 102),
            (7, 100), (7, 101),
            (8, 101), (8, 102),
            (102, 101), (101, 100),
            (0, 3), (0, 4), (99, 3), (99, 1), (99, 2)
        ]
    )

    return graph


def test_should_correctly_transform(
        correct_graph_for_left_side_p6,
        correct_graph_for_p6_right_side,
        production6
):
    subgraph = production6.find_isomorphic_to_left_side(correct_graph_for_left_side_p6)
    production_right_side = production6.apply(correct_graph_for_left_side_p6, subgraph)

    assert _are_graphs_isomorphic(production_right_side, correct_graph_for_p6_right_side)


def test_should_not_transform_removed_node(
        correct_graph_for_left_side_p6,
        correct_graph_for_p6_right_side,
        production6
):
    correct_graph_for_left_side_p6.remove_node(1)
    subgraph = production6.find_isomorphic_to_left_side(correct_graph_for_left_side_p6)
    assert subgraph is None


def test_should_not_transform_removed_edge(
        correct_graph_for_left_side_p6,
        correct_graph_for_p6_right_side,
        production6
):
    correct_graph_for_left_side_p6.remove_edge(2, 4)
    subgraph = production6.find_isomorphic_to_left_side(correct_graph_for_left_side_p6)
    assert subgraph is None


def test_should_not_transform_wrong_node_type(
        correct_graph_for_left_side_p6,
        correct_graph_for_p6_right_side,
        production6
):
    old_node_1 = VertexParams(**correct_graph_for_left_side_p6.nodes[1])

    correct_graph_for_left_side_p6.add_nodes_from([
        (
            1,
            dataclasses.asdict(
                dataclasses.replace(
                    old_node_1, vertex_type=VertexType.INTERIOR
                )
            ),
        )
    ])
    subgraph = production6.find_isomorphic_to_left_side(correct_graph_for_left_side_p6)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        correct_graph_for_left_side_p6,
        correct_graph_for_p6_right_side,
        production6
):
    old_node_14 = VertexParams(**correct_graph_for_left_side_p6.nodes[14])

    correct_graph_for_left_side_p6.add_nodes_from([
        (
            14,
            dataclasses.asdict(
                dataclasses.replace(
                    old_node_14, position=(0.2, 0.69)
                )
            ),
        )
    ])
    subgraph = production6.find_isomorphic_to_left_side(correct_graph_for_left_side_p6)
    assert subgraph is None


def test_should_correctly_transform_bigger_graph(
        bigger_graph_for_p6_left_side,
        bigger_graph_for_p6_right_side,
        production6
):
    subgraph = production6.find_isomorphic_to_left_side(bigger_graph_for_p6_left_side)
    production_graph = production6.apply(bigger_graph_for_p6_left_side, subgraph)
    assert _are_graphs_isomorphic(bigger_graph_for_p6_right_side, production_graph)
