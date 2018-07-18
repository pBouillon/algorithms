import copy
from typing import List, Dict, Set

"""Tabu search implementation

This class allows you to evaluate the best repartition of X tasks of
various weight in several processors so that the final repartition is
as much balanced as possible among processors
"""

def get_initial_state(procs: int, tasks: List[int]) -> Dict[int, List[int]]:
    """generate the initial state of the system

    the initial stage is easy to generate: all processors have an empty 
    tasklist except the first one which has it all

    example:
        {
            0: [1, 2, 2, 2, 2, 3, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 9], 
            1: [], 
            2: []
        }

    :param procs: number of available processors
    :param tasks: list of tasks to distribute

    :return: the initial state
    """
    if procs < 1:
        exit('Must provide at least one processor')

    state = {i: [] for i in range(procs)}
    state[0] = sorted(tasks)

    return state


def get_neighbors(state: Dict[int, List[int]]) -> List[Dict[int, List[int]]]:
    """given a state, return its neighbors

    for each processor, move its task to another processor and add it as 
    neighbor

    :param state: the root state

    :return: list of all neighbors
    """
    neighbors = []

    for source in range(len(state)):
        for task_id in range(len(state[source])):
            for destination in range(len(state)):
                # moving a task to its source is useless
                if destination == source:
                    continue

                # creating the neighbor
                neighbors.append(copy.deepcopy(state))

                # removing the task
                task = neighbors[-1][source].pop(task_id)

                # add it to the other processor
                new_tasklist = neighbors[-1][destination][:]
                new_tasklist.append(task)
                neighbors[-1][destination] = sorted(new_tasklist)

    return neighbors


def fitness(state: Dict[int, List[int]]) -> float:
    """evaluate the fitness of a solution

    calculate the average gap of time between all processors

    :param state: the state to evaluate

    :return: the average gap
    """
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
    """tabu search algorithm

    given a state, evaluate all its neighbor and
    select the best one while the maximum
    iteration is not reached

    :param procs: number of processors
    :param tasks: tasks to sort
    :max_iter: number of iteration to reach before stopping
    :max_size: tabu list size

    :return: the best solution found
    """
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

        # for all neighbors
        for s_candidate in s_neighborhood:

            # if we have not already analysed this solution
            if s_candidate in tabu_list:
                continue

            # select the best candidate of all neighbors
            if fitness(s_candidate) < fitness(best_candidate):
                best_candidate = copy.deepcopy(s_candidate)

        # if the best candidate is better than the best solution
        # it becomes the best solution
        if fitness(best_candidate) < fitness(s_best):
            s_best = copy.deepcopy(best_candidate)

        # adding the best candidate to analysed solutions
        tabu_list.append(copy.deepcopy(best_candidate))

        # adjusting tabu list size
        if len(tabu_list) > max_size:
            tabu_list.pop()

    return s_best


def formatted_result(state: Dict[int, List[int]]) -> str:
    """pretty display for a state

    :param state: state to format

    :return: a string formated to display relevant information
    """
    formatted = ''
    for i in range(len(state)):
        formatted += f'{i}\t|\t{state[i]}\t->\t{sum(state[i])}\n'

    formatted += f'\ndelta: {fitness(state)}'
    return formatted


if __name__ == '__main__':
    tabu_res = tabu_search(
        procs=4,
        tasks=[6, 4, 5, 6, 7, 8, 5, 6, 7, 9, 12, 5, 9, 34, 11, 2, 3, 4, 6 ,21]
    )

    print(formatted_result(tabu_res))
    
    # 0   |   [2, 4, 4, 5, 5, 5, 6, 6, 6] ->  43
    # 1   |   [8, 34] ->  42
    # 2   |   [9, 12, 21] ->  42
    # 3   |   [3, 6, 7, 7, 9, 11] ->  43
    #
    # delta: 2.0

