from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented


# TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action, state) in enumerate(actions_states))
    return value, action


# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    is_terminal_state = game.is_terminal(state)
    if max_depth == 0:
        return heuristic(game, state, 0), None
    if game.get_turn(state) == 0:
        if is_terminal_state[0]:
            return is_terminal_state[1][0], None
        result_value, result_action = float('-inf'), None
        for action in game.get_actions(state):
            value = minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0]
            if value > result_value:
                result_value, result_action = value, action
        return result_value, result_action
    else:
        if is_terminal_state[0]:
            return is_terminal_state[1][1], None
        result_value, result_action = float('inf'), None
        for action in game.get_actions(state):
            value = minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0]
            if value < result_value:
                result_value, result_action = value, action
        return result_value, result_action


def alphabeta_recursive(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'),
                        beta: float = float('inf')) -> Tuple[float, A]:
    is_terminal_state = game.is_terminal(state)
    if max_depth == 0:
        return heuristic(game, state, 0), None
    if game.get_turn(state) == 0:
        if is_terminal_state[0]:
            return is_terminal_state[1][0], None
        result_value, result_action = float('-inf'), None
        for action in game.get_actions(state):
            value = alphabeta_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1, alpha, beta)[0]
            if value >= beta:
                return value, action
            if value > result_value:
                result_value, result_action = value, action
            alpha = max(alpha, result_value)
        return result_value, result_action
    else:
        if is_terminal_state[0]:
            return is_terminal_state[1][1], None
        result_value, result_action = float('inf'), None
        for action in game.get_actions(state):
            value = alphabeta_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1, alpha, beta)[0]
            if value <= alpha:
                return value, action
            if value < result_value:
                result_value, result_action = value, action
            beta = min(beta, result_value)
        return result_value, result_action


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    return alphabeta_recursive(game, state, heuristic, max_depth)


def alphabeta_with_move_ordering_recursive(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1,
                                           alpha: float = float('-inf'),
                                           beta: float = float('inf')) -> Tuple[float, A]:
    is_terminal_state = game.is_terminal(state)
    if max_depth == 0:
        return heuristic(game, state, 0), None
    if game.get_turn(state) == 0:
        if is_terminal_state[0]:
            return is_terminal_state[1][0], None
        result_value, result_action = float('-inf'), None
        heuristic_values = [(heuristic(game, game.get_successor(state, action), 0), action) for action in game.get_actions(state)]
        heuristic_values.sort(key=lambda x: x[0], reverse=True)
        for heuristic_value, action in heuristic_values:
            value = alphabeta_with_move_ordering_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1, alpha, beta)[0]
            if value >= beta:
                return value, action
            if value > result_value:
                result_value, result_action = value, action
            alpha = max(alpha, result_value)
        return result_value, result_action
    else:
        if is_terminal_state[0]:
            return is_terminal_state[1][1], None
        result_value, result_action = float('inf'), None
        heuristic_values = [(heuristic(game, game.get_successor(state, action), 0), action) for action in game.get_actions(state)]
        heuristic_values.sort(key=lambda x: x[0])
        for heuristic_value, action in heuristic_values:
            value = alphabeta_with_move_ordering_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1, alpha, beta)[0]
            if value <= alpha:
                return value, action
            if value < result_value:
                result_value, result_action = value, action
            beta = min(beta, result_value)
        return result_value, result_action


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    return alphabeta_with_move_ordering_recursive(game, state, heuristic, max_depth)


def expectimax_recursive(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    is_terminal_state = game.is_terminal(state)
    if max_depth == 0:
        return heuristic(game, state, 0), None
    if game.get_turn(state) == 0:
        if is_terminal_state[0]:
            return is_terminal_state[1][0], None
        result_value, result_action = float('-inf'), None
        for action in game.get_actions(state):
            value = expectimax_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1)[0]
            if value > result_value:
                result_value, result_action = value, action
        return result_value, result_action
    else:
        if is_terminal_state[0]:
            return is_terminal_state[1][1], None
        actions = game.get_actions(state)
        predicted_action = 0
        for action in actions:
            value = expectimax_recursive(game, game.get_successor(state, action), heuristic, max_depth - 1)[0]
            predicted_action += value
        return predicted_action / len(actions), None


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    return expectimax_recursive(game, state, heuristic, max_depth)
