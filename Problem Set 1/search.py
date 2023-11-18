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
    # frontier is a queue of (state, actions) tuples
    frontier = deque()
    frontier.append((initial_state, []))
    # explored is a set of states
    explored = set()
    while frontier:
        # Get the first element from the frontier
        (state, parent_actions) = frontier.popleft()
        # Check if the state has been explored before
        if state in explored:
            continue
        # Add the state to the explored set
        explored.add(state)
        # Get the actions that can be applied to the current state
        actions = problem.get_actions(state)
        for action in actions:
            current_child_actions = parent_actions.copy()
            current_child_actions.append(action)
            # Get the next state by applying the action to the current state
            next_state = problem.get_successor(state, action)
            # Check if the next state is the goal state
            if problem.is_goal(next_state):
                return current_child_actions
            # Add the next state to the frontier
            frontier.append((next_state, current_child_actions))
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # frontier is a stack of (state, actions) tuples
    frontier = deque()
    frontier.append((initial_state, []))
    # explored is a set of states
    explored = set()
    while frontier:
        # Get the first element from the frontier
        (state, parent_actions) = frontier.pop()
        # Check if the state has been explored before
        if state in explored:
            continue
        # Add the state to the explored set
        explored.add(state)
        # Check if the state is the goal state
        if problem.is_goal(state):
            return parent_actions
        # Get the actions that can be applied to the current state
        actions = problem.get_actions(state)
        for action in actions:
            current_child_actions = parent_actions.copy()
            current_child_actions.append(action)
            # Get the next state by applying the action to the current state
            next_state = problem.get_successor(state, action)
            # Add the next state to the frontier
            frontier.append((next_state, current_child_actions))
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # frontier is a priority queue of (cost, state, actions) tuples
    frontier = []
    order = 1  # To prevent comparing states (Which causes an error) and to make sure that the order of the states is correct
    heapq.heappush(frontier, (0, 0, initial_state, []))
    # explored is a set of states
    explored = set()
    while frontier:
        # Get the first element from the frontier
        (cost, _id, state, parent_actions) = heapq.heappop(frontier)
        # Check if the state has been explored before
        if state in explored:
            continue
        # Add the state to the explored set
        explored.add(state)
        # Check if the state is the goal state
        if problem.is_goal(state):
            return parent_actions
        # Get the actions that can be applied to the current state
        actions = problem.get_actions(state)
        for action in actions:
            current_child_actions = parent_actions.copy()
            current_child_actions.append(action)
            # Get the next state by applying the action to the current state
            next_state = problem.get_successor(state, action)
            # Add the next state to the frontier
            heapq.heappush(frontier, (cost + problem.get_cost(state, action), order, next_state, current_child_actions))
            # Increment the order
            order += 1
    return None


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    frontier = []
    order = 1  # To prevent comparing states (Which causes an error) and to make sure that the order of insertion is preserved
    heapq.heappush(frontier, (heuristic(problem, initial_state), 0, initial_state, []))
    explored = set()
    while frontier:
        (cost, _id, state, parent_actions) = heapq.heappop(frontier)
        if state in explored:
            continue
        explored.add(state)
        if problem.is_goal(state):
            return parent_actions
        actions = problem.get_actions(state)
        for action in actions:
            current_child_actions = parent_actions.copy()
            current_child_actions.append(action)
            next_state = problem.get_successor(state, action)
            heapq.heappush(frontier, (
                heuristic(problem, next_state) - heuristic(problem, state) + cost + problem.get_cost(state, action),
                order, next_state,
                current_child_actions))
            order += 1
    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    frontier = []
    order = 1  # To prevent comparing states (Which causes an error) and to make sure that the order of insertion is preserved
    heapq.heappush(frontier, (0.0, 0, initial_state, []))
    explored = set()
    while frontier:
        (cost, _id, state, parent_actions) = heapq.heappop(frontier)
        if state in explored:
            continue
        explored.add(state)
        if problem.is_goal(state):
            return parent_actions
        actions = problem.get_actions(state)
        for action in actions:
            current_child_actions = parent_actions.copy()
            current_child_actions.append(action)
            next_state = problem.get_successor(state, action)
            heapq.heappush(frontier, (heuristic(problem, next_state), order, next_state, current_child_actions))
            order += 1
    return None
