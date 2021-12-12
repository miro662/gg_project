import pytest
from collections import Counter
from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import (
    start_graph,
    graph_after_first_production,
    production1,
    production2,
)


@pytest.mark.skip(reason="Production 1 not implemented")
def test_matches_isomorphism_in_unbroken_triangle_graph(
    unbroken_triangle_graph, production2
):
    # when
    subgraph = production2.find_isomorphic_to_left_side(unbroken_triangle_graph)

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
