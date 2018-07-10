import copy
from typing import List, Dict, Set


def get_initial_state(procs: int, tasks: List[int]) -> Dict[int, List[int]]:
    if procs < 1:
        exit('Must provide at least one processor')

    state = {i: [] for i in range(procs)}
    state[0] = sorted(tasks)

    return state


def get_neighbors(state: Dict[int, List[int]]) -> List[Dict[int, List[int]]]:
    neighbors = []

    for source in range(len(state)):
        for task_id in range(len(state[source])):
            for destination in range(len(state)):
                if destination == source:
                    continue

                neighbors.append(copy.deepcopy(state))

                task = neighbors[-1][source].pop(task_id)
                neighbors[-1][destination].append(task)

    return neighbors


def fitness(state: Dict[int, List[int]]) -> float:
    avg = sum([sum(state[i]) for i in range(len(state))])
    avg /= len(state)

    sums = [sum(state[i]) for i in range(len(state))]
    return sum(abs(avg - record) for record in sums)


def tabu_search(
        procs: int,
        tasks: List[int],
        max_iter: int = 1000,
        max_size: int = 100
) -> Dict[int, List[int]]:
    # generating initial state
    s0 = get_initial_state(procs, tasks)

    # initializing
    s_best = copy.deepcopy(s0)
    best_candidate = copy.deepcopy(s0)

    # initializing tabu list
    tabu_list = [copy.deepcopy(s0)]

    for _ in range(max_iter):
        s_neighborhood = get_neighbors(best_candidate)
        best_candidate = s_neighborhood[0]

        for s_candidate in s_neighborhood:

            if s_candidate in tabu_list:
                continue

            if fitness(s_candidate) < fitness(best_candidate):
                best_candidate = copy.deepcopy(s_candidate)

        if fitness(best_candidate) < fitness(s_best):
            s_best = copy.deepcopy(best_candidate)

        tabu_list.append(copy.deepcopy(best_candidate))

        if len(tabu_list) > max_size:
            tabu_list.pop()

    return s_best


def formatted_result(state: Dict[int, List[int]]) -> str:
    formatted = ''
    for i in range(len(state)):
        formatted += f'{i}\t|\t{state[i]}\t->\t{sum(state[i])}\n'

    formatted += f'\ndelta: {fitness(state)}'
    return formatted


if __name__ == '__main__':
    print(formatted_result(tabu_search(
        procs=3,
        tasks=[2, 6, 4, 5, 6, 7, 8, 5, 2, 5, 6, 1, 2, 3, 2, 7, 9]
    )))
