# -*- coding: utf-8 -*-
"""
    dijkstra
    --------

    Dijkstra shortest path implementation.

    :authors: Bouillon Pierre.
    :licence: MIT, see LICENSE for more details.
"""
from typing import List

from algorithms.dijkstra.graph import Graph


def get_default_graph() -> Graph:
    """Generate a basic graph to work with

    Representation:

              ____ A ___
          3 /      |     \ 4
           /       |      \
       s =         | 1      = t
           \       |      /
          6 \ ____ B ___ / 2


    :return: the generated graph
    """
    graph = Graph()
    graph.set_distance('s', {'A': 3, 'B': 6})
    graph.set_distance('A', {'B': 1, 't': 4})
    graph.set_distance('B', {'t': 2})
    graph.set_distance('t', {})
    return graph


def dijkstra(graph: Graph, source: str, target: str) -> List[str]:
    """Find the shortest path between `source` and `target`

    :param graph: the graph to work on
    :param source: the source node
    :param target: the target node
    :return: a list of the edges from the `source` to the `target` resulting in
             the shortest path
    """
    # if their is no searches to do
    if source == target:
        return [source]

    # initializing all distances to inf and the start to 0
    distance = {edge: float('inf') for edge in graph.edges}
    distance[source] = 0

    # keeping track of the ancestors
    ancestor = {edge: edge for edge in graph.edges}

    # nodes to parse
    open_nodes = graph.edges[:]

    # while we can search through the nodes
    while open_nodes:
        # looking at the node with the smallest distance
        current_node = min(open_nodes, key=distance.get)

        # removing this node from future researches
        open_nodes.remove(current_node)

        # for each child of the selected node
        for child in graph.get_children(current_node):
            # evaluating the new distance
            new_distance = distance[current_node] + graph.get_distance(
                current_node,
                child
            )

            # if the new distance is shortest than the current one
            # update it and keep track of its predecessor
            if new_distance < distance[child]:
                distance[child] = new_distance
                ancestor[child] = current_node

    # rebuilding the path
    path = []
    current_node = target

    # from the end, rebuilding the path to the source
    while current_node != source:
        path.append(current_node)
        current_node = ancestor[current_node]

    # add the source as final destination, then reverse the path
    return [*path, source][::-1]
