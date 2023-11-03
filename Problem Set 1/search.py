from typing import Tuple, List

from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import heapq


# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    frontier = deque()
    dummy_actions: Tuple[S, List[A]] = []
    frontier.append((initial_state, dummy_actions))
    explored = set()
    while frontier:
        (state, parent_actions) = frontier.pop()
        if state in explored:
            continue
        explored.add(state)
        if problem.is_goal(state):
            return parent_actions
        actions = problem.get_actions(state)
        child_actions = parent_actions.copy()
        for action in actions:
            current_child_actions = child_actions.copy()
            current_child_actions.append(action)
            next_state = problem.get_successor(state, action)
            frontier.append((next_state, current_child_actions))
    print("No solution found")
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()
