"""Contains code for visualising generated graphs

Should be used from a jupyter notebook as shown in example.ipynb
"""
from typing import Iterator

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from gg_project.vertex_params import VertexType

COLOR_MAPPING = {
    VertexType.START: "red",
    VertexType.START_USED: "red",
    VertexType.EXTERIOR: "blue",
    VertexType.INTERIOR: "orange",
    VertexType.INTERIOR_USED: "brown",
}


def draw(
    graph, level=None, figsize=None, titlesize=24, nodesize=500, fontsize=20
) -> None:
    """Draws the given graph using matplotlib

    :param graph: graph which will b drawn
    :param level: the level which will be drawn (all if given None)
    :param figsize: figsize of the drawn figure
    :param titlesize: size of the figure title
    :param nodesize: size of the nodes
    :param fontsize: size of the node labels
    """
    # pylint: disable=too-many-arguments
    nodelist = [
        i for i, node in graph.nodes.items() if level is None or node["level"] == level
    ]

    subgraph = graph.subgraph(nodelist)

    nodes = subgraph.nodes
    pos = {i: _position(subgraph, node, i) for i, node in nodes.items()}
    labels = {i: node["vertex_type"].value for i, node in nodes.items()}
    color = [COLOR_MAPPING[nodes[i]["vertex_type"].value] for i in nodelist]

    fig = plt.figure(figsize=figsize)
    title = f"Siatka na poziomie {level}" if level is not None else "Siatka"
    axes = fig.add_axes([0, 0, 1, 1])
    axes.set_title(title, fontsize=titlesize)

    nx.draw_networkx(
        subgraph,
        nodelist=nodelist,
        pos=pos,
        labels=labels,
        node_color=color,
        ax=axes,
        node_size=nodesize,
        font_size=fontsize,
        font_color="white",
    )


def _position(graph: nx.Graph, node: dict, i: int) -> tuple[float, float]:
    """Calculate the position where a given node should be drawn

    :param graph: graph where the given node is present
    :param node: node whose position will be calculated
    :param i: index of this node in the given graph

    :returns: the drawing coordinates for the given node
    """
    # pylint: disable=invalid-name
    level = node["level"]
    level_nodes = [i for i, node in graph.nodes.items() if node["level"] == level]
    level_graph = graph.subgraph(level_nodes)

    if node["position"] is not None:
        (x, y) = node["position"]
        if _nodes_at_position(level_graph, (x, y)) > 1:
            [x, y] = [x, y] + np.sum(
                (_neighbor_positions(level_graph, i) - (x, y)) / 15, axis=0
            )

    else:
        [x, y] = np.mean(_neighbor_positions(level_graph, i), axis=0)

    return (x, -(y + 2 * level))


def _nodes_at_position(graph: nx.Graph, pos: tuple[float, float]) -> int:
    """Returns the number of nodes present at the given position"""
    count = 0

    for _, node in graph.nodes.items():
        count += 1 if node["position"] == pos else 0

    return count


def _neighbor_positions(graph: nx.Graph, i: int) -> np.ndarray:
    """Returns positions of neighbors of the given node"""
    return np.array(
        [
            neighbor["position"]
            for neighbor in _neighbors(graph, i)
            if neighbor["position"] is not None
        ]
    )


def _neighbors(graph: nx.Graph, i: int) -> Iterator[dict]:
    """Returns an iterator over neighbors of the given node"""
    for j in nx.neighbors(graph, i):
        yield graph.nodes[j]
