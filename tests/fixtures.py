import dataclasses

import networkx as nx
import pytest

from gg_project.productions.p1 import Production1
from gg_project.productions.p2 import Production2
from gg_project.productions.p3 import Production3
from gg_project.productions.p5 import Production5
from gg_project.productions.p6 import Production6
from gg_project.productions.p7 import Production7
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
                        vertex_type=VertexType.START, position=(0.5, 0.5), level=0
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
def production2():
    return Production2()

  
@pytest.fixture
def production3():
    return Production3()

@pytest.fixture
def production5():
    return Production5()

  
@pytest.fixture
def production6():
    return Production6()
  
  
@pytest.fixture
def production7():
    return Production7()


@pytest.fixture
def graph_after_first_production(start_graph, production1):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=1
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),
            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),
        ]
    )

    return G


@pytest.fixture
def graph_after_second_production(start_graph, production2):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2
                    )
                ),
            ),
            (
                8,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2
                    )
                ),
            ),
            (
                9,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                10,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
            (
                11,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                12,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),
            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),
            (5, 11),
            (5, 12),
            (7, 11),
            (7, 12),
            (10, 11),
            (10, 12),
            (7, 10),
            (7, 8),
            (7, 9),
            (8, 10),
            (9, 10),
            (8, 11),
            (8, 12),
        ]
    )

    return G


@pytest.fixture
def graph_before_seventh_production(start_graph, production1):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2
                    )
                ),
            ),
            (
                8,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2
                    )
                ),
            ),
            (
                9,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                10,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
            (
                11,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                12,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),

            (
                14,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                15,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2
                    )
                ),
            ),
            (
                16,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
            (
                17,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                18,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),
            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),
            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),
            (5, 11),
            (5, 12),
            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),
            (6, 17),
            (8, 15),
            (14, 15),
            (16, 17),
            (14, 17),
            (15, 17),
            (16, 14),
            (16, 8),
            (16, 18),
            (8, 18),
            (15, 18),
            (6, 18),
            (16, 15)
        ]
    )

    return G


@pytest.fixture
def graph_after_seventh_production(start_graph, production1):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2
                    )
                ),
            ),
            (
                8,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2
                    )
                ),
            ),
            (
                11,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                12,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                15,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2
                    )
                ),
            ),

            (
                17,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                18,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                19,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                20,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 6),
            (5, 11),
            (5, 12),
            (6, 17),
            (7, 8),
            (7, 11),
            (7, 12),
            (7, 19),
            (7, 20),
            (8, 11),
            (8, 15),
            (8, 18),
            (8, 19),
            (11, 19),
            (12, 19),
            (12, 20),
            (15, 17),
            (15, 18),
            (15, 20),
            (17, 19),
            (17, 20),
            (18, 19),
            (19, 20),
        ]
    )

    return G
