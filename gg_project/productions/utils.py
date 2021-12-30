import networkx as nx

from gg_project.vertex_params import VertexParams, VertexType


def all_neighbors_of_type(
        graph: nx.Graph, node_id: int, vertex_type: VertexType
) -> bool:
    neighbor_types = (
        VertexParams(**graph.nodes[neighbor_id]).vertex_type
        for neighbor_id in graph.neighbors(node_id)
    )
    return all(neighbor_type == vertex_type for neighbor_type in neighbor_types)
