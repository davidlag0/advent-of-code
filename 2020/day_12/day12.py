#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone
expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a
route directly to safety, it produced extremely circuitous instructions. When the captain uses the
PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions
paired with integer input values. After staring at them for a few minutes, you work out what they
probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing.
(That is, if the ship is facing east and the next instruction is N10, the ship would move north 10
units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17,
north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its
east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that
location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings
were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of
degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of
degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative
to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving
the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship
remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving
the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10
units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving
the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between
that location and the ship's starting position?
'''

from __future__ import annotations
import os
from typing import Iterable, Dict
import unittest


INPUT_FILENAME = 'day_12_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input_file:
        return map(str.strip, input_file.readlines())

class Ship:
    '''Class that represents a ship and its position'''

    DIRECTIONS = {
        0: ['x', +1],
        90: ['y', -1],
        180: ['x', -1],
        270: ['y', +1]
    }

    def __init__(self):
        self.__x_axis = 0
        self.__y_axis = 0
        self.__angle = 0

    def update_position(self, action: str) -> Ship:
        '''Update the position of the ship using the provided action information'''

        if action[0] == 'N':
            self.__y_axis += int(action[1:])
        elif action[0] == 'S':
            self.__y_axis -= int(action[1:])
        elif action[0] == 'E':
            self.__x_axis += int(action[1:])
        elif action[0] == 'W':
            self.__x_axis -= int(action[1:])
        elif action[0] == 'L':
            self.__angle = (self.__angle - int(action[1:])) % 360
        elif action[0] == 'R':
            self.__angle = (self.__angle + int(action[1:])) % 360
        elif action[0] == 'F':
            if self.DIRECTIONS[self.__angle][0] == 'x':
                self.__x_axis = self.__x_axis + self.DIRECTIONS[self.__angle][1] * int(action[1:])
            elif self.DIRECTIONS[self.__angle][0] == 'y':
                self.__y_axis = self.__y_axis + self.DIRECTIONS[self.__angle][1] * int(action[1:])

        return self

    def update_position_with_values(self, x_axis: int, y_axis: int) -> Ship:
        '''Update the position of the ship using the provided axis delta values'''
        self.__x_axis += x_axis
        self.__y_axis += y_axis
        return self

    def get_position(self) -> Dict[str, int]:
        '''Get the position of the ship'''

        return {'x': self.__x_axis, 'y': self.__y_axis, 'angle': self.__angle}


class Waypoint:
    '''Class that represents a waypoint around a ship'''

    CLOCKWISE_ROTATIONS = {
        0: ['NO_SWAP', +1, +1],
        90: ['SWAP', +1, -1],
        180: ['NO_SWAP', -1, -1],
        270: ['SWAP', -1, +1]
    }

    COUNTER_CLOCKWISE_ROTATIONS = {
        0: ['NO_SWAP', +1, +1],
        90: ['SWAP', -1, +1],
        180: ['NO_SWAP', -1, -1],
        270: ['SWAP', +1, -1]
    }

    def __init__(self):
        self.__x_axis = 10
        self.__y_axis = 1
        self.ship = Ship()

    def update_position(self, action: str) -> Waypoint:
        '''Update the position of the waypoint using the provided action information'''

        if action[0] == 'N':
            self.__y_axis += int(action[1:])
        elif action[0] == 'S':
            self.__y_axis -= int(action[1:])
        elif action[0] == 'E':
            self.__x_axis += int(action[1:])
        elif action[0] == 'W':
            self.__x_axis -= int(action[1:])
        elif action[0] == 'L':
            if self.COUNTER_CLOCKWISE_ROTATIONS[int(action[1:])][0] == 'SWAP':
                self.__x_axis, self.__y_axis = self.__y_axis, self.__x_axis

            self.__x_axis *= self.COUNTER_CLOCKWISE_ROTATIONS[int(action[1:])][1]
            self.__y_axis *= self.COUNTER_CLOCKWISE_ROTATIONS[int(action[1:])][2]
        elif action[0] == 'R':
            if self.CLOCKWISE_ROTATIONS[int(action[1:])][0] == 'SWAP':
                self.__x_axis, self.__y_axis = self.__y_axis, self.__x_axis

            self.__x_axis *= self.CLOCKWISE_ROTATIONS[int(action[1:])][1]
            self.__y_axis *= self.CLOCKWISE_ROTATIONS[int(action[1:])][2]
        elif action[0] == 'F':
            self.ship.update_position_with_values(self.__x_axis * int(action[1:]),
                                      self.__y_axis * int(action[1:]))

        return self

    def get_position(self) -> Dict[str, int]:
        '''Get the position of the waypoint'''

        return {'x': self.__x_axis, 'y': self.__y_axis}

    def get_ship_position(self) -> Dict[str, int]:
        '''Get the position of the ship related to the waypoint'''

        return self.ship.get_position()


def solve_part1(filename: str) -> int:
    '''Solve Part 1 of the daily puzzle'''
    ship = Ship()

    for action in load_input_file(filename):
        ship.update_position(action)

    return abs(ship.get_position()['x']) + abs(ship.get_position()['y'])


def solve_part2(filename: str) -> int:
    '''Solve Part 1 of the daily puzzle'''
    waypoint = Waypoint()

    for action in load_input_file(filename):
        waypoint.update_position(action)

    return abs(waypoint.get_ship_position()['x']) + abs(waypoint.get_ship_position()['y'])


class Tests(unittest.TestCase):
    '''Tests'''

    ship_test_action_cases = (
        ('F10', {'x': 10, 'y': 0, 'angle': 0}, {'x': 10, 'y': 0, 'angle': 0}),
        ('N3', {'x': 0, 'y': 3, 'angle': 0}, {'x': 10, 'y': 3, 'angle': 0}),
        ('F7', {'x': 7, 'y': 0, 'angle': 0}, {'x': 17, 'y': 3, 'angle': 0}),
        ('R90', {'x': 0, 'y': 0, 'angle': 90}, {'x': 17, 'y': 3, 'angle': 90}),
        ('F11', {'x': 11, 'y': 0, 'angle': 0}, {'x': 17, 'y': -8, 'angle': 90}),
    )

    def test_individual_ship_actions(self):
        '''Test each individual ship action of the test group'''

        for case in self.ship_test_action_cases:
            with self.subTest(case[0]):
                result = Ship().update_position(case[0]).get_position()
                self.assertEqual(result, case[1])

    def test_suite_of_ship_actions(self):
        '''Test the final ship result after multiple ship actions'''
        ship = Ship()

        for case in self.ship_test_action_cases:
            with self.subTest(case[0]):
                result = ship.update_position(case[0]).get_position()
                self.assertEqual(result, case[2])

    waypoint_test_action_cases = (
        ('F10', {'x': 10, 'y': 1}, {'x': 10, 'y': 1}, {'x': 100, 'y': 10, 'angle': 0}),
        ('N3', {'x': 10, 'y': 4}, {'x': 10, 'y': 4}, {'x': 100, 'y': 10, 'angle': 0}),
        ('F7', {'x': 10, 'y': 1}, {'x': 10, 'y': 4}, {'x': 170, 'y': 38, 'angle': 0}),
        ('R90', {'x': 1, 'y': -10}, {'x': 4, 'y': -10}, {'x': 170, 'y': 38, 'angle': 0}),
        ('F11', {'x': 10, 'y': 1}, {'x': 4, 'y': -10}, {'x': 214, 'y': -72, 'angle': 0}),
    )

    def test_individual_waypoint_actions(self):
        '''Test each individual waypoint action of the test group'''

        for case in self.waypoint_test_action_cases:
            with self.subTest(case[0]):
                result = Waypoint().update_position(case[0]).get_position()
                self.assertEqual(result, case[1])

    def test_suite_of_waypoint_actions(self):
        '''Test the final ship result after multiple ship actions'''
        waypoint = Waypoint()

        for case in self.waypoint_test_action_cases:
            with self.subTest(case[0]):
                waypoint_result = waypoint.update_position(case[0]).get_position()
                ship_result = waypoint.get_ship_position()
                self.assertEqual(waypoint_result, case[2])
                self.assertEqual(ship_result, case[3])


if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f'Part 1: {solve_part1(INPUT_FILENAME)}')
    print(f'Part 2: {solve_part2(INPUT_FILENAME)}')
