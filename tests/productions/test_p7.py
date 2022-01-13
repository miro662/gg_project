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
    graph_after_applying = production7.apply(graph_before_seventh_production, None)

    assert _are_graphs_matching(graph_after_applying, graph_after_seventh_production)
