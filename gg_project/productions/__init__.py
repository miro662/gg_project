""" Module containing productions
"""

import abc

import networkx as nx


class Production(abc.ABC):
    """A single production"""

    @abc.abstractmethod
    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        """Find one subgraph isomorphic to the left side of production

        :param graph: graph in which isomorphic subgraph will be searched for

        :returns: subgraph view that matches the left side of production or None
                  if isomorphic subgraph is not found
        """

    @abc.abstractmethod
    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        """Apply production to graph in the position denoted by subgraph

        :param graph:    graph on which production will be applied
        :param subgraph: subgraph denoting the position in which to apply the production

        :returns: _new_ graph with production applied
        """
