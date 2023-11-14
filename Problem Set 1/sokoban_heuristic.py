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

# A function that perform bfs from a given point to a given point
# Sets all path to the goal to 0 and all other points to the maximum value
def bfs(start: Point, goal: Point, layout: SokobanLayout) -> List[int]:
    visited = [[0 for i in range(layout.width)] for j in range(layout.height)]
    queue = deque()
    visited[start.y][start.x] = 0
    queue.append((start, [start]))
    while queue:
        (point, path) = queue.popleft()
        for direction in Direction:
            new_point = point + direction.to_vector()
            if new_point in layout.walkable and visited[new_point.y][new_point.x] == 0:
                visited[new_point.y][new_point.x] = 1
                queue.append((new_point, [new_point] + path))
                if new_point == goal:
                    return [new_point] + path
    return []


def calc_cost_zero_max(problem: SokobanProblem, state: SokobanState, graph: dict[Point, List[List[int]]]) -> List[
    List[int]]:
    current_goals = set(problem.layout.goals)
    current_crates = set(state.crates)
    result_graph = [[1000 for i in range(problem.layout.width)] for j in range(problem.layout.height)]
    for goal in current_goals:
        closest_crate = None
        closest_crate_distance = 10000
        for crate in current_crates:
            if graph[goal][crate.y][crate.x] < closest_crate_distance:
                closest_crate_distance = graph[goal][crate.y][crate.x]
                closest_crate = crate
        path = bfs(closest_crate, goal, problem.layout)
        start = 0.1
        for point in path:
            result_graph[point.y][point.x] = start
            # start += 0.1
        current_crates.remove(closest_crate)
    for crate in state.crates:
        other_crates = set(state.crates)
        other_crates.remove(crate)
        for direction in Direction:
            new_point = crate + direction.to_vector()
            if new_point + Direction.LEFT.to_vector() in problem.layout.walkable:
                result_graph[new_point.y][new_point.x - 1] = 0.1
            if new_point + Direction.RIGHT.to_vector() in problem.layout.walkable:
                result_graph[new_point.y][new_point.x + 1] = 0.1
            if new_point not in problem.layout.walkable or new_point in other_crates:
                result_graph[new_point.y][new_point.x] = 0.1
                for direction2 in Direction:
                    new_point2 = new_point + direction2.to_vector()
                    if new_point2 in problem.layout.walkable:
                        result_graph[new_point2.y][new_point2.x] = 0.1
    for goal in problem.layout.goals:
        result_graph[goal.y][goal.x] = 0
    print()
    for i in range(problem.layout.height):
        for j in range(problem.layout.width):
            if result_graph[i][j] == 1000:
                print("#", end="")
            else:
                print(".", end="")
        print()
    return result_graph


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


def bfs_flod_fill_all(layout: SokobanLayout) -> List[List[int]]:
    area = layout.width * layout.height
    graph = [[area for i in range(layout.width)] for j in range(layout.height)]
    queue = deque()
    for goal in layout.goals:
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


def get_cost(problem: SokobanProblem, state: SokobanState, graph: dict[Point, List[List[int]]]) -> int:
    cost = 0
    current_goals = set(problem.layout.goals)
    current_crates = set(problem.layout.goals)
    for goal in current_goals:
        closest_crate = None
        closest_crate_distance = 10000
        for crate in current_crates:
            if graph[goal][crate.y][crate.x] < closest_crate_distance:
                closest_crate_distance = graph[goal][crate.y][crate.x]
                closest_crate = crate
        cost += closest_crate_distance
        current_crates.remove(closest_crate)
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
        cache['graph'] = flod_fill_goals(problem.layout)
        cache['graph_zero_max'] = calc_cost_zero_max(problem, state, cache['graph'])
        cache['graph_all'] = bfs_flod_fill_all(problem.layout)
        # for l in cache['graph_zero_max']:
        #     print(l)
    graph = cache['graph']
    graph_all = cache['graph_all']
    graph_zero_max = cache['graph_zero_max']
    is_dead_lock = check_dead_lock(problem.layout, state)
    # return min(manhattan_distance(state.player, crate) for crate in state.crates) + sum(
    #     [min([manhattan_distance(crate, goal) for goal in problem.layout.goals]) for crate in
    #      state.crates]) - 1 + 100 * is_dead_lock
    # return max(sum(graph_zero_max[crate.y][crate.x] for crate in state.crates),
    #            sum(graph_all[crate.y][crate.x] for crate in state.crates)) + 10000 * is_dead_lock
    return sum(graph_zero_max[crate.y][crate.x] for crate in state.crates) + 10000 * is_dead_lock
