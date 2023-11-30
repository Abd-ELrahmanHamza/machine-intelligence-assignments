from typing import Any, Dict, List, Optional, Tuple
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented


# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable


# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min(
        (len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if
        variable in domains)
    return variable


# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    # TODO: Write this function
    for constraint in problem.constraints:
        # Check if the constraint is binary constraint
        if not isinstance(constraint, BinaryConstraint):
            continue
        # Check if the assigned variable belongs to this constraint
        if assigned_variable not in constraint.variables:
            continue
        # Get the other variable
        other_variable = constraint.get_other(assigned_variable)
        # Check if the other variable is assigned
        if other_variable not in domains:
            continue
        # Update the other variable's domain
        new_domain = {value for value in domains[other_variable] if constraint.condition(assigned_value, value)}
        if not new_domain:
            return False
        domains[other_variable] = new_domain
    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    # TODO: Write this function
    restraining_values: List[Tuple] = []
    for value in domains[variable_to_assign]:
        domain_size = 0
        for constraint in problem.constraints:
            if not isinstance(constraint, BinaryConstraint):
                continue
            # check if the variable belongs to this constraint
            if variable_to_assign not in constraint.variables:
                continue
            # get the other variable
            other_variable = constraint.get_other(variable_to_assign)
            # check if the other variable is assigned
            if other_variable not in domains:
                continue
            # get the other variable's domain
            new_domain = {value for value in domains[other_variable] if constraint.condition(value, value)}
            domain_size += len(new_domain)
        # add the value and its domain size to the list
        restraining_values.append((domain_size, value))
    # sort the list
    restraining_values.sort()
    # return the values only
    return [value for _, value in restraining_values]


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    # TODO: Write this function
    # Apply 1-Consistency
    solvable = one_consistency(problem)
    if not solvable:
        return None
    # Solve the problem
    return backtracking_search(problem, problem.domains, {})


def backtracking_search(problem: Problem, domains: Dict[str, set], assignment: Assignment) -> Optional[Assignment]:
    # Check if the assignment is complete
    if problem.is_complete(domains):
        return assignment
    # Select the variable to assign next
    variable_to_assign = minimum_remaining_values(problem, domains)
    # Get the values of the variable in the order of the least constraining value heuristic
    values = least_restraining_values(problem, variable_to_assign, domains)
    # Try assigning each value
    for value in values:
        # Create a copy of the domains to be used by forward checking
        domains = domains.copy()
        # Assign the value to the variable and remove it from the domains
        domains.pop(variable_to_assign)
        # Add the assignment to the assignment
        assignment[variable_to_assign] = value
        # Apply forward checking
        if forward_checking(problem, variable_to_assign, value, domains):
            # If forward checking succeeds, solve the problem recursively
            solution = backtracking_search(problem, domains, assignment)
            if solution is not None:
                return solution
    # If no solution was found, return None
    return None
