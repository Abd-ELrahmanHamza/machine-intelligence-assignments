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

def flod_fill(layout: SokobanLayout) -> List[List[int]]:
    area = layout.width * layout.height
    graph = [[area for i in range(layout.width)] for j in range(layout.height)]

    def bfs_flod_fill():
        queue = deque()
        for goal in layout.goals:
            queue.append(goal)
            graph[goal.y][goal.x] = 0
        while queue:
            point = queue.popleft()
            for direction in Direction:
                new_point = point + direction.to_vector()
                if new_point in layout.walkable and graph[new_point.y][new_point.x] == area:
                    graph[new_point.y][new_point.x] = graph[point.y][point.x] + 1
                    queue.append(new_point)

    bfs_flod_fill()
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


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # cache = problem.cache()
    # if 'graph' not in cache:
    #     cache['graph'] = flod_fill(problem.layout)
    # graph = cache['graph']
    is_dead_lock = check_dead_lock(problem.layout, state, problem)
    return min(manhattan_distance(state.player, crate) for crate in state.crates) + sum(
        [min([manhattan_distance(crate, goal) for goal in problem.layout.goals]) for crate in
         state.crates]) - 1 + 100 * is_dead_lock
