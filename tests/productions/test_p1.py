from gg_project.vertex_params import VertexParams, VertexType
from tests.fixtures import graph_after_first_production, production1, start_graph


def test_finds_first_element_in_start_graph(start_graph, production1):
    # when
    subgraphs = list(production1.find_isomorphic_to_left_side(start_graph))
    subgraph = subgraphs[0]

    # then
    assert len(subgraphs) == 1

    assert subgraph is not None
    assert len(subgraph.nodes) == 1
    assert VertexParams(**subgraph.nodes[0]).vertex_type == VertexType.START


def test_does_not_find_anything_in_non_start_graph(
    graph_after_first_production, production1
):
    # when
    subgraphs = list(
        production1.find_isomorphic_to_left_side(graph_after_first_production)
    )

    # then
    assert len(subgraphs) == 0
