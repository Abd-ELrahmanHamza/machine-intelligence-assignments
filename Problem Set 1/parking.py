from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = List[List[str]]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]


# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[
        Point]  # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]  # A tuple of points where state[i] is the position of car 'i'.
    slots: Dict[
        Point, int]  # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int  # The width of the parking lot.
    height: int  # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        print("cars = ",self.cars)
        initial_state: ParkingState = [['#' for _ in range(self.width)] for _ in range(self.height)]
        for point in self.passages:
            initial_state[point.y][point.x] = '.'
        for car in self.cars:
            initial_state[car.y][car.x] = chr(ord('A') + self.cars.index(car))
        for slot, index in self.slots.items():
            initial_state[slot.y][slot.x] = str(index)
        for l in initial_state:
            print(l)
        return initial_state

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # TODO: ADD YOUR CODE HERE
        for y in range(self.height):
            for x in range(self.width):
                character = state[y][x]
                if character.isalpha() and character != str(self.slots[Point(y, x)]):
                    print("not goal")
                    for l in state:
                        print(l)
                    return False
        return True

    def is_valid_move(self, x: int, y: int, direction: Direction, state: ParkingState) -> bool:
        vector_direction = direction.to_vector()
        new_x = x + vector_direction.x
        new_y = y + vector_direction.y
        if new_x >= self.width or new_x < 0 or new_y >= self.height or new_y < 0:
            return False
        if state[new_y][new_x] != '.':
            return False
        return True

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # TODO: ADD YOUR CODE HERE
        available_actions: List[ParkingAction] = []
        for y in range(self.height):
            for x in range(self.width):
                character: str = state[y][x]
                if character.isalpha():
                    for direction in Direction:
                        if self.is_valid_move(x, y, direction, state):
                            available_actions.append((ord(character) - ord('A'), direction))
        print("available_actions = ", available_actions)
        return available_actions

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        NotImplemented()

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE
        NotImplemented()

    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
