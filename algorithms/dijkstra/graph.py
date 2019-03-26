# -*- coding: utf-8 -*-
"""
    graph
    --------

    Basic graph implementation

    :authors: Bouillon Pierre.
    :licence: MIT, see LICENSE for more details.
"""
import json
from typing import List, Dict


class Graph:
    """References Graph

    Minimal implementation of a graph
    """

    def __init__(self):
        self._graph = dict()

    def __str__(self):
        return json.dumps(self._graph)

    def get_children(self, edge: str) -> List[str]:
        """Get the children of a node

        :param edge: parent node
        :return: a list of the children
        """
        return list(self._graph[edge].keys())

    def get_distance(self, source: str, target: str) -> int:
        """Get the distance from `source` to `target`

        :raise KeyError: on a non-existing edge

        :param source: source edge
        :param target: target edge
        :return: the distance between them as an int
        """
        return self._graph[source][target]

    def set_distance(self, edge: str, distances_to: Dict[str, int]):
        """Add a distance from `edge` to all edges as keys in `distance_to`

        :param edge: source
        :param distances_to: dict as {target: distance_to_target]
        """
        self._graph[edge] = distances_to

    @property
    def edges(self) -> List[str]:
        """Get all edges

        :return: list of edges
        """
        return list(self._graph.keys())
