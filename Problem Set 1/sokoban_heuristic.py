from collections import deque
from typing import List

from sokoban import SokobanProblem, SokobanState, SokobanLayout
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


# TODO: Import any modules and write any functions you want to use

def flod_fill(layout: SokobanLayout, crates) -> (List[List[int]], List[List[int]]):
    area = layout.width * layout.height

    def bfs_flod_fill(goals: frozenset[Point]):
        graph = [[area for i in range(layout.width)] for j in range(layout.height)]
        queue = deque()
        for goal in goals:
            queue.append(goal)
            graph[goal.y][goal.x] = 0
        while queue:
            point = queue.popleft()
            for direction in Direction:
                new_point = point + direction.to_vector()
                if new_point in layout.walkable and graph[new_point.y][new_point.x] == area:
                    graph[new_point.y][new_point.x] = graph[point.y][point.x] + 1
                    queue.append(new_point)
        return graph
    goals_graph = bfs_flod_fill(layout.goals)
    crates_graph = bfs_flod_fill(crates)
    return goals_graph, crates_graph


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    cache = problem.cache()
    if 'goals_graph' not in cache:
        cache['goals_graph'], cache['crates_graph'] = flod_fill(problem.layout, state.crates)
        # for l in cache['goals_graph']:
        #     print(l)
        # print()
        # for l in cache['crates_graph']:
        #     print(l)
    goals_graph = cache['goals_graph']
    crates_graph = cache['crates_graph']

    # if player is surrounded by crates
    surrounded_crate = False
    for direction in Direction:
        if state.player + direction.to_vector() in state.crates:
            surrounded_crate = True
            break
    if surrounded_crate:
        return max(goals_graph[crate.y][crate.x] for crate in state.crates)
    return max(crates_graph[crate.y][crate.x] for crate in state.crates)
