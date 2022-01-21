import dataclasses

import networkx as nx
import pytest

from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import production3


def _are_nodes_equal(node1, node2) -> bool:
    return VertexParams(**node1) == VertexParams(**node2)


def _are_graphs_isomorphic(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    return nx.is_isomorphic(
        graph1,
        graph2,
        node_match=_are_nodes_equal
    )


@pytest.fixture
def correct_graph_for_left_side_p3():
    graph = nx.Graph()
    graph.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                )
            ),
        ),
        (
            1,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                )
            ),
        ),
        (
            2,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                )
            ),
        ),
        (
            3,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1
                )
            ),
        ),
        (
            4,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR, position=(1 / 3, 2 / 3), level=1
                )
            ),
        ),
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 0),
        (4, 1),
        (4, 2)
    ])

    return graph


@pytest.fixture
def correct_graph_for_p3_right_side():
    graph = nx.Graph()
    graph.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 0.0),
                    level=1
                )
            )
        ),
        (
            1,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 1.0),
                    level=1
                )
            )
        ),
        (
            2,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 1.0),
                    level=1
                )
            )
        ),
        (
            3,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.5, 0.5),
                    level=1
                )
            )
        ),
        (
            4,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR_USED,
                    position=(1 / 3, 2 / 3),
                    level=1
                )
            )
        ),
        (
            5,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(1 / 6, 0.5),
                    level=2
                )
            )
        ),
        (
            6,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(0.5, 5 / 6),
                    level=2
                )
            )
        ),
        (
            7,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 0.0),
                    level=2
                )
            )
        ),
        (
            8,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 1.0),
                    level=2
                )
            )
        ),
        (
            9,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 1.0),
                    level=2
                )
            )
        ),
        (
            10,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.5, 0.5),
                    level=2
                )
            )
        )
    ])

    graph.add_edges_from([
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 4),
        (2, 3),
        (2, 4),
        (4, 5),
        (4, 6),
        (5, 7),
        (5, 8),
        (5, 10),
        (6, 8),
        (6, 9),
        (6, 10),
        (7, 8),
        (7, 10),
        (8, 9),
        (8, 10),
        (9, 10)
    ])

    return graph


@pytest.fixture
def bigger_graph_for_p3_left_side():
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=(1 / 6, 0.5), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=(0.5, 5 / 6), level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=(2 / 3, 0.5), level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (7, 0),
            (7, 2),
            (7, 3),
            (6, 0),
            (6, 1),
            (6, 2),
            (4, 0),
            (4, 7),
            (4, 3),
            (5, 7),
            (5, 3),
            (5, 2)
        ]
    )

    return G


@pytest.fixture
def bigger_graph_for_p3_right_side():
    graph = nx.Graph()
    graph.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 0.0),
                    level=1
                )
            )
        ),
        (
            1,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 0.0),
                    level=1
                )
            )
        ),
        (
            2,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 1.0),
                    level=1
                )
            )
        ),
        (
            3,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 1.0),
                    level=1
                )
            )
        ),
        (
            4,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(1 / 6, 0.5),
                    level=1
                )
            )
        ),
        (
            5,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(0.5, 5 / 6),
                    level=1
                )
            )
        ),
        (
            6,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR_USED,
                    position=(2 / 3, 0.5),
                    level=1
                )
            )
        ),
        (
            7,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.5, 0.5),
                    level=1
                )
            )
        ),
        (
            8,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(0.5, 1 / 6),
                    level=2
                )
            )
        ),
        (
            9,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    position=(5 / 6, 0.5),
                    level=2
                )
            )
        ),
        (
            10,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.0, 0.0),
                    level=2
                )
            )
        ),
        (
            11,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 0.0),
                    level=2
                )
            )
        ),
        (
            12,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(1.0, 1.0),
                    level=2
                )
            )
        ),
        (
            13,
            dataclasses.asdict(
                VertexParams(
                    vertex_type=VertexType.EXTERIOR,
                    position=(0.5, 0.5),
                    level=2
                )
            )
        ),
    ])

    graph.add_edges_from([
        (0, 1),
        (0, 3),
        (0, 7),
        (0, 6),
        (0, 4),
        (1, 2),
        (1, 6),
        (2, 3),
        (2, 7),
        (2, 6),
        (2, 5),
        (3, 7),
        (3, 4),
        (3, 5),
        (4, 7),
        (5, 7),
        (6, 8),
        (6, 9),
        (8, 10),
        (8, 11),
        (8, 13),
        (9, 11),
        (9, 12),
        (9, 13),
        (10, 11),
        (10, 13),
        (11, 12),
        (11, 13),
        (12, 13)
    ])

    return graph


def test_should_correctly_transform(
        correct_graph_for_left_side_p3,
        correct_graph_for_p3_right_side,
        production3
):
    subgraph = production3.find_isomorphic_to_left_side(correct_graph_for_left_side_p3)
    production_right_side = production3.apply(correct_graph_for_left_side_p3, subgraph)

    assert _are_graphs_isomorphic(production_right_side, correct_graph_for_p3_right_side)


def test_should_not_transform_removed_node(
        correct_graph_for_left_side_p3,
        correct_graph_for_p3_right_side,
        production3
):
    correct_graph_for_left_side_p3.remove_node(0)
    subgraph = production3.find_isomorphic_to_left_side(correct_graph_for_left_side_p3)
    assert subgraph is None


def test_should_not_transform_removed_edge(
        correct_graph_for_left_side_p3,
        correct_graph_for_p3_right_side,
        production3
):
    correct_graph_for_left_side_p3.remove_edge(0, 1)
    subgraph = production3.find_isomorphic_to_left_side(correct_graph_for_left_side_p3)
    assert subgraph is None


def test_should_not_transform_wrong_node_type(
        correct_graph_for_left_side_p3,
        correct_graph_for_p3_right_side,
        production3
):
    old_node_0 = VertexParams(**correct_graph_for_left_side_p3.nodes[0])

    correct_graph_for_left_side_p3.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                dataclasses.replace(
                    old_node_0, vertex_type=VertexType.INTERIOR
                )
            ),
        )
    ])
    subgraph = production3.find_isomorphic_to_left_side(correct_graph_for_left_side_p3)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        correct_graph_for_left_side_p3,
        correct_graph_for_p3_right_side,
        production3
):
    old_node_0 = VertexParams(**correct_graph_for_left_side_p3.nodes[0])

    correct_graph_for_left_side_p3.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                dataclasses.replace(
                    old_node_0, position=(1, 1)
                )
            ),
        )
    ])
    subgraph = production3.find_isomorphic_to_left_side(correct_graph_for_left_side_p3)
    assert subgraph is None


def test_should_correctly_transform_bigger_graph(
        bigger_graph_for_p3_left_side,
        bigger_graph_for_p3_right_side,
        production3
):
    subgraph = production3.find_isomorphic_to_left_side(bigger_graph_for_p3_left_side)
    production_graph = production3.apply(bigger_graph_for_p3_left_side, subgraph)
    assert _are_graphs_isomorphic(bigger_graph_for_p3_right_side, production_graph)
