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
    area = 100000
    graph = [[area for i in range(layout.width)] for j in range(layout.height)]

    # BFS flood fill from goals to determine the smallest distance from each goal to each point in the layout
    # This will be used to determine the distance from each crate to the nearest goal
    # This is the actual distance not only the manhattan distance
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
                    graph[new_point.y][new_point.x] = (graph[point.y][point.x] + 1)
                    queue.append(new_point)

    bfs_flod_fill()
    return graph


def check_dead_lock(layout: SokobanLayout, state: SokobanState, problem: SokobanProblem) -> int:
    # Check if crate is in corner and not on goal
    for crate in state.crates:
        wall_indices = []
        for direction in Direction:
            if crate in problem.layout.goals:
                continue
            wall = crate + direction.to_vector()
            if wall not in layout.walkable:
                wall_indices.append(direction.value)
        wall_indices.sort()
        # Check if crate is in corner (Two adjacent walls beside it)
        for i in range(1, len(wall_indices)):
            if wall_indices[i] - wall_indices[i - 1] == 1:
                return 1
        if len(wall_indices) >= 2 and wall_indices[-1] == 3 and wall_indices[0] == 0:
            return 1
    # Check case if crate is between a wall and another crate
    for crate in state.crates:
        # Check if crate is beside maze outer walls and not on goal
        if crate.x == 1 or crate.x == layout.width - 2:
            # check if there is a crate left or right to it
            if (
                    crate + Direction.LEFT.to_vector() in state.crates) and (
                    crate + Direction.LEFT.to_vector() not in layout.goals or crate not in layout.goals):
                return 1
            if (
                    crate + Direction.RIGHT.to_vector() in state.crates) and (
                    crate + Direction.RIGHT.to_vector() not in layout.goals or crate not in layout.goals):
                return 1
        if crate.y == 1 or crate.y == layout.height - 2:
            # check if there is a crate up or down to it and not on goal
            if (
                    crate + Direction.UP.to_vector() in state.crates) and (
                    crate + Direction.UP.to_vector() not in layout.goals or crate not in layout.goals):
                return 1
            if (
                    crate + Direction.DOWN.to_vector() in state.crates) and (
                    crate + Direction.DOWN.to_vector() not in layout.goals or crate not in layout.goals):
                return 1
    # Check the number of crates beside each wall
    # If the number of crates is more than the number of goals beside the wall then it is a deadlock
    # get number of crates beside each wall
    left_wall_crates = []
    right_wall_crates = []
    upper_wall_crates = []
    lower_wall_crates = []
    for crate in state.crates:
        if crate.x == 1:
            left_wall_crates.append(crate)
        if crate.x == layout.width - 2:
            right_wall_crates.append(crate)
        if crate.y == 1:
            upper_wall_crates.append(crate)
        if crate.y == layout.height - 2:
            lower_wall_crates.append(crate)
    # get number of goals beside each wall
    left_wall_goals = []
    right_wall_goals = []
    upper_wall_goals = []
    lower_wall_goals = []
    for goal in layout.goals:
        if goal.x == 1:
            left_wall_goals.append(goal)
        if goal.x == layout.width - 2:
            right_wall_goals.append(goal)
        if goal.y == 1:
            upper_wall_goals.append(goal)
        if goal.y == layout.height - 2:
            lower_wall_goals.append(goal)
    # Check if the number of crates beside each wall is more than the number of goals beside the wall
    if len(left_wall_crates) > len(left_wall_goals):
        return 1
    if len(right_wall_crates) > len(right_wall_goals):
        return 1
    if len(upper_wall_crates) > len(upper_wall_goals):
        return 1
    if len(lower_wall_crates) > len(lower_wall_goals):
        return 1

    return 0


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
    graph = cache['graph']
    is_dead_lock = check_dead_lock(problem.layout, state, problem)
    res = 100000000 * is_dead_lock
    res += sum(graph[crate.y][crate.x] for crate in state.crates)
    res += (min(manhattan_distance(state.player, crate) for crate in state.crates) - 1)
    # res += sum([min([manhattan_distance(crate, goal) for goal in problem.layout.goals]) for crate in state.crates])
    # res += sum([min([euclidean_distance(crate, goal) for goal in problem.layout.goals]) for crate in state.crates])
    return res
