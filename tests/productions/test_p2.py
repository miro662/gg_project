import pytest
import networkx as nx
from collections import Counter
from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import (
    start_graph,
    graph_after_first_production,
    graph_after_second_production,
    production1,
    production2,
)


def _are_graphs_matching(g1: nx.Graph, g2: nx.Graph) -> bool:
    g1_nodes_values = list(map(lambda n: tuple(n.values()), g1.nodes.values()))
    g2_nodes_values = list(map(lambda n: tuple(n.values()), g2.nodes.values()))
    return Counter(g1_nodes_values) == Counter(g2_nodes_values)


def test_matches_isomorphism_in_graph_after_first_production(
    graph_after_first_production, production2
):
    # when
    subgraph = production2.find_isomorphic_to_left_side(graph_after_first_production)

    # then
    assert subgraph is not None
    assert len(subgraph.nodes) == 4

    type_counts = Counter(
        map(lambda node: VertexParams(**node[1]).vertex_type, subgraph.nodes.items())
    )
    assert type_counts[VertexType.EXTERIOR] == 3
    assert type_counts[VertexType.INTERIOR] == 1


def test_does_not_match_isomorphism_in_start_graph(start_graph, production2):
    # when
    subgraph = production2.find_isomorphic_to_left_side(start_graph)

    # then
    assert subgraph is None


def test_applies_to_graph_after_first_production(
    graph_after_first_production, graph_after_second_production, production2
):
    subgraph = production2.find_isomorphic_to_left_side(graph_after_first_production)
    graph_after_applying = production2.apply(graph_after_first_production, subgraph)

    assert _are_graphs_matching(graph_after_applying, graph_after_second_production)
