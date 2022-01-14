import dataclasses
from typing import Any

import networkx as nx
import pytest

from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import production5


def _get_node(nr: int, vertex_type: VertexType, position: tuple[float, float], level: int) -> tuple[
    int, dict[str, Any]]:
    return (
               nr,
               dataclasses.asdict(
                   VertexParams(vertex_type=vertex_type, position=position, level=level)
               ),
           )


def _are_graphs_isomorphic(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    return nx.is_isomorphic(
        graph1,
        graph2,
        node_match=_are_nodes_equal
    )


def _are_nodes_equal(node1, node2) -> bool:
    return VertexParams(**node1) == VertexParams(**node2)


@pytest.fixture
def correct_graph_for_left_side_p5():
    graph = nx.Graph()
    graph.add_nodes_from([
        _get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        _get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.5), level=1),
        _get_node(2, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        _get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 1.0), level=1),
        _get_node(4, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        _get_node(5, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),
        _get_node(6, vertex_type=VertexType.INTERIOR, position=(1/3, 2/3), level=1)
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),

        (6, 0),
        (6, 2),
        (6, 4)
    ])

    return graph


@pytest.fixture
def correct_graph_for_p5_right_side():
    graph = nx.Graph()
    graph.add_nodes_from([
        _get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        _get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.5), level=1),
        _get_node(2, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        _get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 1.0), level=1),
        _get_node(4, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        _get_node(5, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),

        # _get_node(6, vertex_type=VertexType.INTERIOR, position=(1 / 3, 2 / 3), level=1),
        # _get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        # _get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        # _get_node(2, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        # _get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),

        _get_node(6, vertex_type=VertexType.INTERIOR_USED, position=(1 / 3, 2 / 3), level=1),
        _get_node(7, vertex_type=VertexType.INTERIOR, position=(1 / 6, 0.5), level=2),
        _get_node(8, vertex_type=VertexType.INTERIOR, position=(0.5, 5/6), level=2),
        _get_node(9, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2),
        _get_node(10, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2),
        _get_node(11, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2),
        _get_node(12, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2)
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),

        (6, 0),
        (6, 2),
        (6, 4),
        (6, 8),
        (5, 7),
        (7, 10),
        (7, 12),
        (8, 10),
        (8, 11),
        (8, 12),
        (9, 10),
        (9, 12),
        (10, 11),
        (12, 10),
        (11, 12)
    ])

    return graph


def test_should_correctly_transform(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    production_right_side = production5.apply(correct_graph_for_left_side_p5, subgraph)

    assert subgraph is not None
    assert production_right_side is not None

def test_should_not_transform_removed_edge(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    correct_graph_for_left_side_p5.remove_edge(0, 1)
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    old_node_0 = VertexParams(**correct_graph_for_left_side_p5.nodes[0])

    correct_graph_for_left_side_p5.add_nodes_from([
        (
            0,
            dataclasses.asdict(
                dataclasses.replace(
                    old_node_0, position=(1, 1)
                )
            ),
        )
    ])
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    assert subgraph is None
