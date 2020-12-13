#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes
directly to the tropical island where you can finally start your vacation. As you reach the waiting
area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're
pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your
puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an
occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly. Fortunately, people are
entirely predictable and always follow a simple set of rules. All decisions are based on the
number of occupied seats adjacent to a given seat (one of the eight positions immediately up,
down, left, right, or diagonal from the seat). The following rules are applied to every seat
simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat
becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further applications of
these rules cause no seats to change state! Once people stop moving around, you count 37 occupied
seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?

--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent
seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in
each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied
ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied
seats for an occupied seat to become empty (rather than four or more from the previous rules). The
other rules still apply: empty seats that see no occupied seats become occupied, seats matching no
rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as
follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once
this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once
equilibrium is reached, how many seats end up occupied?
'''

import os
from typing import Iterable, List, Tuple, Dict
import copy
import unittest


TEST_INPUT_FILENAME = 'day_11_test_input.txt'
TEST_ROUND_1_OUTPUT = 'round_1_output.txt'
TEST_ROUND_2_OUTPUT = 'round_2_output.txt'
TEST_ROUND_3_OUTPUT = 'round_3_output.txt'
TEST_ROUND_4_OUTPUT = 'round_4_output.txt'
TEST_ROUND_5_OUTPUT = 'round_5_output.txt'
TEST_ROUND_1_PART2_OUTPUT = 'test_round_1_part2_output.txt'
TEST_ROUND_2_PART2_OUTPUT = 'test_round_2_part2_output.txt'
TEST_ROUND_3_PART2_OUTPUT = 'test_round_3_part2_output.txt'
TEST_ROUND_4_PART2_OUTPUT = 'test_round_4_part2_output.txt'
TEST_ROUND_5_PART2_OUTPUT = 'test_round_5_part2_output.txt'
TEST_ROUND_6_PART2_OUTPUT = 'test_round_6_part2_output.txt'
TEST_VISIBLE_SEATS_1 = 'test_visible_seats_1.txt'
TEST_VISIBLE_SEATS_2 = 'test_visible_seats_2.txt'
TEST_VISIBLE_SEATS_3 = 'test_visible_seats_3.txt'
INPUT_FILENAME = 'day_11_input.txt'
SEAT_STATUS = {
    'floor': '.',
    'empty': 'L',
    'occupied': '#',
}


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file.'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input_file:
        return map(str.strip, input_file.readlines())


def load_matrix(filename: str) -> List[List[int]]:
    '''
    Given a filename, return a seat matrix.
    '''
    seat_matrix = []

    for line in load_input_file(filename):
        seat_matrix.append([seat for seat in line])

    return seat_matrix


def positive(number, floor_number) -> int:
    '''
    Returns a minimum number if a provided number is lower than the minimum number
    otherwise returns the provided number.
    '''
    return number if number > floor_number else floor_number


def get_neighbors(matrix: List[List[str]], position: tuple) -> Tuple[str]:
    '''
    Return a tuple of all neighbor cells' values of a given position.
    '''

    neighbors = []

    for row in range(positive(position[0] - 1, 0), position[0] + 2):
        for column in range(positive(position[1] - 1, 0), position[1] + 2):
            if not ((row == position[0]) and (column == position[1])):
                try:
                    neighbors.append(matrix[row][column])
                except IndexError:
                    continue

    return tuple(neighbors)


def get_visible_seats(matrix: List[List[str]], initial_position: tuple) -> Tuple[str]: # NOSONAR
    '''
    Return a tuple of the first visible seat in each of the 8 directions.
    '''
    visible_seats = []
    valid_seat_statuses = (SEAT_STATUS['occupied'], SEAT_STATUS['empty'])

    # Top
    for position in range(initial_position[0] - 1, -1, -1):
        if matrix[position][initial_position[1]] in valid_seat_statuses:
            visible_seats.append(matrix[position][initial_position[1]])
            break

    # Down
    for position in range(initial_position[0] + 1, len(matrix)):
        try:
            if matrix[position][initial_position[1]] in valid_seat_statuses:
                visible_seats.append(matrix[position][initial_position[1]])
                break
        except IndexError:
            break

    # Left
    for position in range(initial_position[1] - 1, -1, -1):
        if matrix[initial_position[0]][position] in valid_seat_statuses:
            visible_seats.append(matrix[initial_position[0]][position])
            break

    # Right
    for position in range(initial_position[1] + 1, len(matrix[0])):
        try:
            if matrix[initial_position[0]][position] in valid_seat_statuses:
                visible_seats.append(matrix[initial_position[0]][position])
                break
        except IndexError:
            break

    # Top left diagonal
    for row, column in zip(range(initial_position[0] - 1, -1, -1),
                                    range(initial_position[1] - 1, -1, -1)):
        if matrix[row][column] in valid_seat_statuses:
            visible_seats.append(matrix[row][column])
            break

    # Top right diagonal
    for row, column in zip(range(initial_position[0] - 1, -1, -1),
                                    range(initial_position[1] + 1, len(matrix[0]))):
        if matrix[row][column] in valid_seat_statuses:
            visible_seats.append(matrix[row][column])
            break

    # Down left diagonal
    for row, column in zip(range(initial_position[0] + 1, len(matrix)),
                                    range(initial_position[1] - 1, -1, -1)):
        if matrix[row][column] in valid_seat_statuses:
            visible_seats.append(matrix[row][column])
            break

    # Down right diagonal
    for row, column in zip(range(initial_position[0] + 1, len(matrix)),
                                    range(initial_position[1] + 1, len(matrix[0]))):
        if matrix[row][column] in valid_seat_statuses:
            visible_seats.append(matrix[row][column])
            break

    return tuple(visible_seats)


def count_state(neighbors: Tuple[str], position_state: str) -> int:
    '''
    Given a tuple of seats and a position state, returns the count of the position
    in the position state.
    '''

    return sum(map(lambda state: state in position_state, neighbors))


def update_seat_matrix(initial_seat_matrix: List[List[str]],
                       rounds: int = 1,
                       visible_seats_to_empty: int = 4,
                       visible_seats_method: str = 'neighbors') -> Dict[List[List[str]], bool]:
    '''
    Return a tuple that contains the updated seat matrix and if there was any change.
    '''
    starting_seat_matrix = initial_seat_matrix
    seats_visibility_method = get_neighbors if visible_seats_method == 'neighbors' \
                                            else get_visible_seats

    #print(f'initial matrix: {initial_seat_matrix}')

    for _ in range(0, rounds):
        seat_matrix_changed = False
        updated_seat_matrix = []

        for row, seat_row in enumerate(starting_seat_matrix):
            new_row = []

            for column, seat in enumerate(seat_row):
                if (seat == SEAT_STATUS['empty']) and \
                    (count_state(seats_visibility_method(starting_seat_matrix, (row, column)),
                                SEAT_STATUS['occupied']) == 0):

                    new_row.append(SEAT_STATUS['occupied'])
                    seat_matrix_changed = True

                elif (seat == SEAT_STATUS['occupied']) and \
                    (count_state(seats_visibility_method(starting_seat_matrix, (row, column)),
                                                SEAT_STATUS['occupied']) >= visible_seats_to_empty):

                    new_row.append(SEAT_STATUS['empty'])
                    seat_matrix_changed = True

                else:
                    new_row.append(seat)

            updated_seat_matrix.append(new_row)

        starting_seat_matrix = copy.deepcopy(updated_seat_matrix)

    return {'matrix': updated_seat_matrix, 'matrix_updated': seat_matrix_changed}


def count_occupied_seats(seat_matrix: List[List[str]]) -> int:
    '''
    Given a seat matrix, returns the number of occupied seats.
    '''
    number_of_occupied_seats = 0

    for _, row in enumerate(seat_matrix):
        for seat in row:
            if seat == SEAT_STATUS['occupied']:
                number_of_occupied_seats += 1

    return number_of_occupied_seats


def solve_part1(filename: str) -> int:
    '''Solve part 1 of the daily puzzle.'''

    updated_seats = True
    seat_matrix = load_matrix(filename)

    while updated_seats:
        result = update_seat_matrix(seat_matrix)
        seat_matrix = result['matrix']
        updated_seats = result['matrix_updated']

    return count_occupied_seats(seat_matrix)


def solve_part2(filename: str) -> int:
    '''Solve part 2 of the daily puzzle.'''

    updated_seats = True
    seat_matrix = load_matrix(filename)

    while updated_seats:
        result = update_seat_matrix(seat_matrix,
                                    visible_seats_to_empty=5,
                                    visible_seats_method='visible_seats')
        seat_matrix = result['matrix']
        updated_seats = result['matrix_updated']

    return count_occupied_seats(seat_matrix)


class Tests(unittest.TestCase):
    '''Tests'''

    test_seat_matrix = []

    get_neighbors_cases = (
        ((0, 0), ('.', 'L', 'L'), 1, 2),
        ((0, 9), ('L', 'L', 'L'), 0, 3),
        ((9, 0), ('L', '.', '.'), 2, 1),
        ((9, 9), ('.', 'L', 'L'), 1, 2),
        ((3, 3), ('L', '.', 'L', 'L', '.', 'L', 'L', '.'), 3, 5),
    )

    seat_update_rounds_cases = (
        ('1-1', 1, TEST_ROUND_1_OUTPUT, True, 4, 'neighbors'),
        ('1-2', 2, TEST_ROUND_2_OUTPUT, True, 4, 'neighbors'),
        ('1-3', 3, TEST_ROUND_3_OUTPUT, True, 4, 'neighbors'),
        ('1-4', 4, TEST_ROUND_4_OUTPUT, True, 4, 'neighbors'),
        ('1-5', 5, TEST_ROUND_5_OUTPUT, True, 4, 'neighbors'),
        ('1-6', 6, TEST_ROUND_5_OUTPUT, False, 4, 'neighbors'),
        ('2-1', 1, TEST_ROUND_1_PART2_OUTPUT, True, 5, 'visible_seats'),
        ('2-2', 2, TEST_ROUND_2_PART2_OUTPUT, True, 5, 'visible_seats'),
        ('2-3', 3, TEST_ROUND_3_PART2_OUTPUT, True, 5, 'visible_seats'),
        ('2-4', 4, TEST_ROUND_4_PART2_OUTPUT, True, 5, 'visible_seats'),
        ('2-5', 5, TEST_ROUND_5_PART2_OUTPUT, True, 5, 'visible_seats'),
        ('2-6', 6, TEST_ROUND_6_PART2_OUTPUT, True, 5, 'visible_seats'),
    )

    visible_seats_cases = (
        (1, TEST_VISIBLE_SEATS_1, (4, 3), ('#', '#', '#', '#', '#', '#', '#', '#'), 0, 8),
        (2, TEST_VISIBLE_SEATS_2, (1, 1), ('L',), 1, 0),
        (3, TEST_VISIBLE_SEATS_3, (3, 3), (), 0, 0),
        (4, TEST_ROUND_1_PART2_OUTPUT, (0, 0), ('#', '#', '#'), 0, 3),
    )

    @classmethod
    def setUpClass(cls):
        for line in load_input_file(TEST_INPUT_FILENAME):
            cls.test_seat_matrix.append([seat for seat in line])

    @classmethod
    def tearDownClass(cls):
        cls.test_seat_matrix = None

    def test_get_neighbors(self):
        '''Test the get_neighbors function.'''
        for case in self.get_neighbors_cases:
            with self.subTest(case[0]):
                result = get_neighbors(self.test_seat_matrix, case[0])
                self.assertEqual(result, case[1])

    def test_count_state_floor(self):
        '''Test the count_state function.'''
        for case in self.get_neighbors_cases:
            with self.subTest(case[0]):
                result = count_state(get_neighbors(self.test_seat_matrix, case[0]),
                                     SEAT_STATUS['floor'])
                self.assertEqual(result, case[2])

    def test_count_state_empty_seat(self):
        '''Test the count_state function.'''
        for case in self.get_neighbors_cases:
            with self.subTest(case[0]):
                result = count_state(get_neighbors(self.test_seat_matrix, case[0]),
                                     SEAT_STATUS['empty'])
                self.assertEqual(result, case[3])

    def test_seat_update_rounds(self):
        '''Verify the seat configuration after multiple rounds.'''
        for case in self.seat_update_rounds_cases:
            with self.subTest(case[0]):
                result = update_seat_matrix(load_matrix(TEST_INPUT_FILENAME),
                                            case[1],
                                            visible_seats_to_empty=case[4],
                                            visible_seats_method=case[5])
                test_matrix = load_matrix(case[2])

                self.assertEqual(result['matrix'], test_matrix)
                self.assertEqual(result['matrix_updated'], case[3])

    def test_count_number_occupied_seats(self):
        '''Test the count_occupied_seats function.'''
        result = count_occupied_seats(update_seat_matrix(load_matrix(TEST_INPUT_FILENAME),
                                                         5)['matrix'])
        self.assertEqual(result, 37)

    def test_get_visible_seats(self):
        '''Test the get_visible_seats function.'''
        for case in self.visible_seats_cases:
            with self.subTest(case[0]):
                result = get_visible_seats(load_matrix(case[1]), case[2])
                self.assertEqual(result, case[3])
                self.assertEqual(count_state(result, SEAT_STATUS['empty']), case[4])
                self.assertEqual(count_state(result, SEAT_STATUS['occupied']), case[5])


if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f'Part 1: {solve_part1(INPUT_FILENAME)}')
    print(f"Part 2: {solve_part2(INPUT_FILENAME)}")
