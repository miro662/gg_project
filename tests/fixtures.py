import dataclasses

import networkx as nx
import pytest

from gg_project.productions.p1 import Production1
from gg_project.vertex_params import VertexParams, VertexType


@pytest.fixture
def start_graph():
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START, position=(0.0, 0.0), level=0
                    )
                ),
            )
        ]
    )
    return G


@pytest.fixture
def production1():
    return Production1()


@pytest.fixture
def graph_after_first_production(start_graph, production1):
    subgraph = next(production1.find_isomorphic_to_left_side(start_graph))
    return production1.apply(start_graph, subgraph)
