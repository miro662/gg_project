# pylint: disable = invalid-name, too-many-locals, fixme

""" Implementation of production number 2

Authors:
Mirosław Błazej
Grzegorz Wcisło
Karol Szuster
"""

import collections
import contextlib
import copy
import dataclasses
import itertools
import math
from typing import Sequence
import networkx as nx
from gg_project.vertex_params import VertexParams, VertexType
from gg_project.productions import Production


NodeId = int


Node = collections.namedtuple("Node", ["id", "params"])


def _all_neighbors_of_type(
    graph: nx.Graph, node_id: NodeId, vertex_type: VertexType
) -> bool:
    neighbor_types = (
        VertexParams(**graph.nodes[neighbor_id]).vertex_type
        for neighbor_id in graph.neighbors(node_id)
    )
    return all(neighbor_type == vertex_type for neighbor_type in neighbor_types)


def _next_node_id(graph: nx.Graph) -> NodeId:
    # This gets called a lot but whatever
    return max(graph.nodes) + 1


def _node_distance(params1: VertexParams, params2: VertexParams) -> float:
    x1, y1 = params1.position
    x2, y2 = params2.position
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x * x + y * y)


def _find_hypotenuse_nodes(triangle_graph_nodes: Sequence[Node]) -> tuple[Node, Node]:
    assert len(triangle_graph_nodes) == 3

    return min(
        itertools.combinations(triangle_graph_nodes, 2),
        key=lambda node_pair: _node_distance(node_pair[0].params, node_pair[1].params),
    )


def _node_line_middle(
    params1: VertexParams, params2: VertexParams
) -> tuple[float, float]:
    x1, y1 = params1.position
    x2, y2 = params2.position
    return (x1 + x2) / 2, (y1 + y2) / 2


def _move_down_node(params: VertexParams, new_id: int) -> Node:
    return Node(new_id, dataclasses.replace(params, level=params.level + 1))


def _create_middle_node(graph: nx.Graph, node1: Node, node2: Node) -> Node:
    mid_x, mid_y = _node_line_middle(node1.params, node2.params)
    return Node(_next_node_id(graph), dataclasses.replace(node1, x=mid_x, y=mid_y))


def _move_down_nodes(graph: nx.Graph, nodes: Sequence[Node]) -> Sequence[Node]:
    return list(
        map(lambda node: _move_down_node(node.params, _next_node_id(graph)), nodes)
    )


def _create_edges(
    used_internal_node: Node,
    hypotenuse_middle_node: Node,
    new_right_angle_node: Node,
    new_internal_nodes: Sequence[Node],
    new_hypotenuse_nodes: Sequence[Node],
) -> Sequence[tuple[NodeId, NodeId]]:
    return [
        (used_internal_node.id, new_internal_nodes[0].id),
        (used_internal_node.id, new_internal_nodes[1].id),
        (new_internal_nodes[0].id, new_hypotenuse_nodes[0].id),
        (new_internal_nodes[0].id, new_right_angle_node.id),
        (new_internal_nodes[0].id, hypotenuse_middle_node.id),
        (new_internal_nodes[1].id, new_hypotenuse_nodes[1].id),
        (new_internal_nodes[1].id, new_right_angle_node.id),
        (new_internal_nodes[1].id, hypotenuse_middle_node.id),
        (hypotenuse_middle_node.id, new_hypotenuse_nodes[0].id),
        (hypotenuse_middle_node.id, new_hypotenuse_nodes[1].id),
        (hypotenuse_middle_node.id, new_right_angle_node.id),
        (new_right_angle_node.id, new_hypotenuse_nodes[0].id),
        (new_right_angle_node.id, new_hypotenuse_nodes[1].id),
    ]


class Production2(Production):
    """Implementation of second production from documentation.

    This production takes an unbroken triangle tile from a graph and produces a new break.
    """

    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        for node_id, params in graph.nodes.items():
            if (VertexParams(**params)).vertex_type != VertexType.INTERIOR:
                continue

            if not _all_neighbors_of_type(graph, node_id, VertexType.EXTERIOR):
                continue

            with contextlib.suppress(nx.NetworkXNoCycle):
                nx.find_cycle(graph, graph.subgraph(graph.neighbors(node_id)))
                return graph.subgraph([node_id, *graph.neighbors(node_id)])

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        assert len(subgraph.nodes) == 4

        new_graph = copy.deepcopy(graph)
        subgraph_nodes: list[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                subgraph.nodes.items(),
            )
        )
        # For now assume the first node of subgraph is the internal node
        # (which is true but ugly)
        internal_node = subgraph_nodes[0]
        new_level = internal_node.params.level + 1
        used_internal_node = Node(
            internal_node.id,
            dataclasses.replace(internal_node.id, vertex_type=VertexType.INTERIOR_USED),
        )
        new_internal_nodes = [
            Node(
                _next_node_id(graph),
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    level=new_level,
                    position=(0.0, 0.0),
                ),
            ),
            Node(
                _next_node_id(graph),
                VertexParams(
                    vertex_type=VertexType.INTERIOR,
                    level=new_level,
                    position=(0.0, 0.0),
                ),
            ),
        ]

        external_nodes = subgraph_nodes[1:]
        hypotenuse_nodes = _find_hypotenuse_nodes(external_nodes)
        right_angle_node = list(set(external_nodes) - set(hypotenuse_nodes))

        hypotenuse_middle_node = _create_middle_node(graph, *hypotenuse_nodes)
        new_hypotenuse_nodes = _move_down_nodes(graph, hypotenuse_nodes)
        [new_right_angle_node] = _move_down_nodes(graph, right_angle_node)

        new_level_nodes: list[Node] = [
            hypotenuse_middle_node,
            new_right_angle_node,
            used_internal_node,
            *new_internal_nodes,
            *new_hypotenuse_nodes,
        ]
        new_level_raw_nodes = map(
            lambda node: (node.id, dataclasses.asdict(node.params)), new_level_nodes
        )
        # FIXME: Make it nicer ( ͡° ͜ʖ ͡°)
        new_level_edges = _create_edges(
            used_internal_node,
            hypotenuse_middle_node,
            new_right_angle_node,
            new_internal_nodes,
            new_hypotenuse_nodes,
        )

        new_graph.add_nodes_from(new_level_raw_nodes)
        new_graph.add_nodes_from(new_level_edges)

        return new_graph
