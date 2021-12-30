import networkx as nx

from gg_project.vertex_params import VertexParams, VertexType


def _get_neighbors(
        graph: nx.Graph, node_id: int
):
    return [
        VertexParams(**graph.nodes[neighbor_id])
        for neighbor_id in graph.neighbors(node_id)
    ]


def _all_neighbors_of_type(
        graph: nx.Graph, node_id: int, vertex_type: VertexType
) -> bool:
    neighbor_types = map(lambda x: x.vertex_type, _get_neighbors(graph, node_id))
    return all(neighbor_type == vertex_type for neighbor_type in neighbor_types)
