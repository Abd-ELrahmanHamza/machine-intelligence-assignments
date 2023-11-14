import heapq
from collections import deque
from typing import List

from sokoban import SokobanProblem, SokobanState, SokobanLayout
from mathutils import Direction, Point, manhattan_distance, euclidean_distance
from helpers.utils import NotImplemented


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


# TODO: Import any modules and write any functions you want to use

def bfs_flod_fill(goal: Point, width: int, height: int, walkable: set[Point]):
    area = width * height
    graph = [[area for i in range(width)] for j in range(height)]
    queue = deque()
    queue.append(goal)
    graph[goal.y][goal.x] = 0
    while queue:
        point = queue.popleft()
        for direction in Direction:
            new_point = point + direction.to_vector()
            if new_point in walkable and graph[new_point.y][new_point.x] == area:
                graph[new_point.y][new_point.x] = round(graph[point.y][point.x] + 0.2, 3)
                queue.append(new_point)
    return graph


def flod_fill(layout: SokobanLayout) -> dict[Point, list[list[int]]]:
    graph = {}
    for goal in layout.goals:
        graph[goal] = bfs_flod_fill(goal, layout.width, layout.height, layout.walkable)
    return graph


def flod_fill_crates(layout: SokobanLayout, state: SokobanState) -> dict[Point, list[list[int]]]:
    graph = {}
    for crate in state.crates:
        walkable = set(layout.walkable)
        for crate_ in state.crates:
            if crate != crate_:
                walkable.remove(crate_)
        graph[crate] = bfs_flod_fill(crate, layout.width, layout.height, walkable)
    return graph


def check_dead_lock(layout: SokobanLayout, state: SokobanState, problem: SokobanProblem) -> int:
    for crate in state.crates:
        wall_indices = []
        for direction in Direction:
            if crate in problem.layout.goals:
                continue
            wall = crate + direction.to_vector()
            if wall not in layout.walkable:
                wall_indices.append(direction.value)
        wall_indices.sort()
        for i in range(1, len(wall_indices)):
            if wall_indices[i] - wall_indices[i - 1] == 1:
                return 1
        if len(wall_indices) >= 2 and wall_indices[-1] == 3 and wall_indices[0] == 0:
            return 1
    return 0


def compute_cost(graph: dict[Point, list[list[int]]], state: SokobanState, problem: SokobanProblem) -> int:
    cost = 0
    cost_queue = []
    dummy = 0
    for crate in state.crates:
        for goal in problem.layout.goals:
            heapq.heappush(cost_queue, (graph[goal][crate.y][crate.x], dummy, crate, goal))
            dummy += 1
    current_goals = set(problem.layout.goals)
    current_crates = set(state.crates)
    while cost_queue:
        (c, dummy, crate, goal) = heapq.heappop(cost_queue)
        if goal in current_goals and crate in current_crates:
            cost += c
            current_goals.remove(goal)
            current_crates.remove(crate)
            # print(goal, crate, c)
    # print("cost: ", cost)
    return cost


def compute_cost_crates(state: SokobanState, problem: SokobanProblem) -> int:
    graph: dict[Point, list[list[int]]] = flod_fill_crates(problem.layout, state)
    cost = 0
    cost_queue = []
    dummy = 0
    for goal in problem.layout.goals:
        for crate in state.crates:
            heapq.heappush(cost_queue, (graph[crate][goal.y][goal.x], dummy, crate, goal))
            dummy += 1
    # print("cost_queue: ", cost_queue)
    current_goals = set(problem.layout.goals)
    current_crates = set(state.crates)
    while cost_queue:
        (c, dummy, crate, goal) = heapq.heappop(cost_queue)
        if goal in current_goals and crate in current_crates:
            cost += c
            current_goals.remove(goal)
            current_crates.remove(crate)
            # print(goal, crate, c)
    # print("cost: ", cost)
    return cost


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    cache = problem.cache()
    if 'graph' not in cache:
        cache['graph'] = flod_fill(problem.layout)
        # for goal in problem.layout.goals:
        #     for l in cache['graph'][goal]:
        #         print(l)
        #     print()
    graph = cache['graph']

    is_dead_lock = check_dead_lock(problem.layout, state, problem)
    res = 10000 * is_dead_lock
    # res += sum(graph[crate.y][crate.x] for crate in state.crates)
    # res += (min(manhattan_distance(state.player, crate) for crate in state.crates) - 1)
    res += compute_cost(graph, state, problem)
    # res += compute_cost_crates(state, problem)
    # res += sum([min([manhattan_distance(crate, goal) for goal in problem.layout.goals]) for crate in state.crates])
    # res += sum([min([euclidean_distance(crate, goal) for goal in problem.layout.goals]) for crate in state.crates])
    return res
