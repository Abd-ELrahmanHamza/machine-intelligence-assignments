from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint


# TODO (Optional): Import any builtin library or define any helper function you want to use

def equal_constraint(x, y):
    # sum_x = 0
    # while x > 0:
    #     sum_x += x % 10
    #     x //= 10
    return sum([int(i) for i in str(x)]) == y


def create_constraint_with_aux(problem, var1, var2):
    aux = var1 + var2
    # var1 is the first variable in the constraint
    problem.constraints.append(BinaryConstraint((var1, aux), lambda x, y: x == y // 10))
    # var2 is the second variable in the constraint
    problem.constraints.append(BinaryConstraint((var2, aux), lambda x, y: x == y % 10))
    # Add the auxiliary variable to the problem variables
    problem.variables.append(aux)
    # Add the auxiliary variable to the problem domains
    problem.domains[aux] = set()
    for i in problem.domains[var1]:
        for j in problem.domains[var2]:
            problem.domains[aux].add(10 * i + j)


def create_constraints(problem: Problem, LHS0, LHS1, Carries, RHS) -> None:
    iterations = len(RHS)
    for i in range(iterations):
        # Create the constraints for the first iteration
        create_constraint_with_aux(problem, Carries[i], LHS0[i])
        create_constraint_with_aux(problem, Carries[i] + LHS0[i], LHS1[i])
        create_constraint_with_aux(problem, Carries[i + 1], RHS[i])
        problem.constraints.append(
            BinaryConstraint((Carries[i] + LHS0[i] + LHS1[i], Carries[i + 1] + RHS[i]), lambda x, y: sum([int(i) for i in str(x)]) == int(y)))


# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i + 1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        padd_of_LHS0 = ["V" + str(i) for i in range(len(RHS) - len(LHS0))]
        padd_of_LHS1 = ["G" + str(i) for i in range(len(RHS) - len(LHS1))]
        # Padd the LHS0 to the length of RHS with V1 as the padding value
        LHS0_Padded = list(reversed(LHS0)) + padd_of_LHS0
        # Padd the LHS1 to the length of RHS with V2 as the padding value
        LHS1_Padded = list(reversed(LHS1)) + padd_of_LHS1
        # Create Auxiliary variables with the length of the RHS with values C0, C1, C2, ... , Cn
        Carries = [f"C{i}" for i in range(len(RHS) + 1)]
        # Convert RHS to list
        RHS_Padded = list(reversed(RHS))
        # Add the variables to the problem variables
        problem.variables.extend(set(LHS0_Padded + LHS1_Padded + Carries + RHS_Padded))

        var_const = list(set(LHS0 + LHS1 + RHS))

        # Add a binary contraint for each pair of variables to be unique
        range_i = range(len(var_const))
        for i in range_i:
            range_j = range(i + 1, len(var_const))
            for j in range_j:
                problem.constraints.append(BinaryConstraint((var_const[i], var_const[j]), lambda x, y: x != y))
        # Apply unary constraints on the variables to restrict the domain of the variables to be in the range [0,9]
        set_10, set_2 = set(range(10)), set(range(2))
        for var in var_const:
            problem.domains[var] = set_10
        for var in Carries:
            problem.domains[var] = set_2
        for var in padd_of_LHS0:
            problem.domains[var] = {0}
        for var in padd_of_LHS1:
            problem.domains[var] = {0}
        # First element of the Carries must be 0
        problem.domains[Carries[0]] = {0}
        problem.domains[Carries[-1]] = {0}
        # Last element of the RHS LSH0 and LSH1 must be in the range [1,9]
        problem.domains[RHS[0]] = set(range(1, 10))
        problem.domains[LHS0[0]] = set(range(1, 10))
        problem.domains[LHS1[0]] = set(range(1, 10))

        create_constraints(problem, LHS0_Padded, LHS1_Padded, Carries, RHS_Padded)
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
