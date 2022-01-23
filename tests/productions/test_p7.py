import dataclasses

import pytest
import networkx as nx
from collections import Counter
from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import (
    start_graph,
    graph_after_first_production,
    graph_after_second_production,
    graph_before_seventh_production,
    graph_after_seventh_production,
    production1,
    production2,
    production7,
)


def _are_graphs_matching(g1: nx.Graph, g2: nx.Graph) -> bool:
    g1_nodes_values = list(map(lambda n: tuple(n.values()), g1.nodes.values()))
    g2_nodes_values = list(map(lambda n: tuple(n.values()), g2.nodes.values()))
    return Counter(g1_nodes_values) == Counter(g2_nodes_values)


def test_applies_to_graph_after_first_production(
        graph_before_seventh_production, graph_after_seventh_production, production7
):
    subgraph = production7.find_isomorphic_to_left_side(graph_before_seventh_production)
    graph_after_applying = production7.apply(graph_before_seventh_production, subgraph)

    assert _are_graphs_matching(graph_after_applying, graph_after_seventh_production)


def test_should_not_transform_removed_node(
        graph_before_seventh_production,
        production7
):
    graph_before_seventh_production.remove_node(10)
    subgraph = production7.find_isomorphic_to_left_side(graph_before_seventh_production)
    assert subgraph is None


def test_should_not_transform_removed_edge(
        graph_before_seventh_production,
        production7
):
    graph_before_seventh_production.remove_edge(6, 17)
    subgraph = production7.find_isomorphic_to_left_side(graph_before_seventh_production)
    assert subgraph is None


def test_should_not_transform_wrong_node_type(
        graph_before_seventh_production,
        production7
):
    old_node_1 = VertexParams(**graph_before_seventh_production.nodes[10])

    graph_before_seventh_production.add_nodes_from(
        [(10, dataclasses.asdict(dataclasses.replace(old_node_1, vertex_type=VertexType.INTERIOR)),)])
    subgraph = production7.find_isomorphic_to_left_side(graph_before_seventh_production)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        graph_before_seventh_production,
        production7
):
    old_node_14 = VertexParams(**graph_before_seventh_production.nodes[14])

    graph_before_seventh_production.add_nodes_from([(14, dataclasses.asdict(dataclasses.replace(old_node_14, position=(0.2, 0.69))),)])
    subgraph = production7.find_isomorphic_to_left_side(graph_before_seventh_production)
    assert subgraph is None
