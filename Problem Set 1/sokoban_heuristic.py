from collections import deque
from typing import List, Dict

from sokoban import SokobanProblem, SokobanState, SokobanLayout
from mathutils import Direction, Point, manhattan_distance, euclidean_distance
from helpers.utils import NotImplemented


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


# TODO: Import any modules and write any functions you want to use

def bfs_flod_fill(goal: Point, layout: SokobanLayout) -> List[List[int]]:
    area = layout.width * layout.height
    graph = [[area for i in range(layout.width)] for j in range(layout.height)]
    queue = deque()
    graph[goal.y][goal.x] = 0
    queue.append(goal)
    while queue:
        point = queue.popleft()
        for direction in Direction:
            new_point = point + direction.to_vector()
            if new_point in layout.walkable and graph[new_point.y][new_point.x] == area:
                graph[new_point.y][new_point.x] = graph[point.y][point.x] + 1
                queue.append(new_point)
    return graph


def flod_fill_goals(layout: SokobanLayout) -> dict[Point, List[List[int]]]:
    goals_graphs = {}
    for goal in layout.goals:
        graph = bfs_flod_fill(goal, layout)
        goals_graphs[goal] = graph
    return goals_graphs


def get_cost(goals_graphs: dict[Point, List[List[int]]], state: SokobanState, problem: SokobanProblem) -> int:
    # get list of (cost, goal,crate) for each crate
    empty_goals = set(problem.layout.goals)
    empty_crates = set(state.crates)
    for goal in problem.layout.goals:
        for crate in state.crates:
            if crate == goal:
                empty_goals.remove(goal)
                empty_crates.remove(crate)
                break
    costs = []
    for goal in empty_goals:
        for crate in empty_crates:
            costs.append((goals_graphs[goal][crate.y][crate.x], goal, crate))
    if len(costs) == 0:
        print("same cost is empty goal")
        return 0
    # sort list by cost if equal sort by nearest goal to the player
    costs.sort(
        key=lambda x: (x[0], manhattan_distance(Point(0, 0), x[1]), goals_graphs[x[1]][state.player.y][state.player.x]))
    # get list of items that have the same cost and goal point
    same_cost = [costs[0]]
    for i in range(len(costs) - 1):
        if costs[i][0] == costs[i + 1][0] and costs[i][1] == costs[i + 1][1]:
            same_cost.append(costs[i + 1])
        else:
            break
    # get a dictionary of (crate,flod_fill) for each crate
    crate_graphs = {}
    for item in same_cost:
        crate_graphs[item[2]] = bfs_flod_fill(item[2], problem.layout)
    # get the crate at which the player has the least flood fill to reach
    min_cost = 100000
    min_crate = None
    for crate in empty_crates:
        if crate not in crate_graphs:
            continue
        cost = crate_graphs[crate][state.player.y][state.player.x]
        if cost < min_cost:
            min_cost = cost
            min_crate = crate
    if len(same_cost) == 0 and len(costs) > 0:
        return min_cost - 1
    print("min_crate = ", min_crate)
    # return the cost of the crate with the least flood fill added to the cost of the goal
    return min_cost - 1 + goals_graphs[same_cost[0][1]][min_crate.y][min_crate.x]


def check_dead_lock(layout: SokobanLayout, state: SokobanState):
    for crate in state.crates:
        wall_indices = []
        for direction in Direction:
            if crate + direction.to_vector() not in layout.walkable:
                wall_indices.append(direction.value)
        wall_indices.sort()
        for i in range(1, len(wall_indices)):
            if wall_indices[i] - wall_indices[i - 1] == 1:
                return 0
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
    cache = problem.cache()
    if 'graph' not in cache:
        cache['graph'] = flod_fill_goals(problem.layout)
    graph = cache['graph']
    is_dead_lock = check_dead_lock(problem.layout, state)
    return get_cost(graph, state, problem) + 1000 * is_dead_lock
