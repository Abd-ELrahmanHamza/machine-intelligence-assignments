from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]

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

    def convert_state_to_grid(self, state: ParkingState) -> List[List[str]]:
        grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if Point(x, y) in self.passages:
                    grid[y][x] = '.'
        for i, car in enumerate(state):
            x, y = car
            grid[y][x] = chr(i + ord('A'))
        return grid

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        initial_state: ParkingState = self.cars
        return initial_state

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # TODO: ADD YOUR CODE HERE
        for car_index, car in enumerate(state):
            if car not in self.slots:
                return False
            if car_index != self.slots[car]:
                return False
        return True

    def is_valid_move(self, car_position: Point, direction: Direction, state: ParkingState) -> bool:
        vector_direction = direction.to_vector()
        new_car_position = car_position + vector_direction
        # Check for not wall
        if new_car_position not in self.passages:
            return False
        # Check for not other car
        if new_car_position in state:
            return False
        return True

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # TODO: ADD YOUR CODE HERE
        available_actions: List[ParkingAction] = []
        for car_index, car in enumerate(state):
            for direction in Direction:
                if self.is_valid_move(car, direction, state):
                    available_actions.append((car_index, direction))
        return available_actions

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        car_index, direction = action
        # Get the current position of the car
        car_position = state[car_index]
        # Move the car to the new position
        vector_direction = direction.to_vector()
        new_car_position = car_position + vector_direction
        new_state = list(state)
        new_state[car_index] = new_car_position
        return tuple(new_state)

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE
        car_index, direction = action
        # Get the current position of the car
        car_position = state[car_index]
        # Move the car to the new position
        vector_direction = direction.to_vector()
        new_car_position = car_position + vector_direction
        # Check if the car is moving to another car parking slot
        if new_car_position in self.slots:
            # Check if the car is moving to its parking slot
            if self.slots[new_car_position] == car_index:
                return 26 - car_index
            # The car is moving to another car parking slot
            return 100 + 26 - car_index
        return 26 - car_index

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
