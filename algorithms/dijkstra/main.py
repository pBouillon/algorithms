from algorithms.dijkstra.dijkstra import get_default_graph, dijkstra


def main():
    graph = get_default_graph()
    shortest_path = dijkstra(graph, 's', 't')

    print(f'working with the graph:\n\t{graph}')
    print(f'shortest path:\n\t{shortest_path}')


if __name__ == '__main__':
    main()
