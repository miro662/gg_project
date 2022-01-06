""" Module containing productions
"""

import abc
from typing import Iterator

import networkx as nx


class Production(abc.ABC):
    """A single production"""

    @classmethod
    @abc.abstractmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> Iterator[nx.Graph]:
        """Find one subgraph isomorphic to the left side of production

        :param graph: graph in which isomorphic subgraph will be searched for

        :returns: iteratio over all subgraph views that matches the left side of production
        """

    @classmethod
    @abc.abstractmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        """Apply production to graph in the position denoted by subgraph

        :param graph:    graph on which production will be applied
        :param subgraph: subgraph denoting the position in which to apply the production

        :returns: _new_ graph with production applied
        """
