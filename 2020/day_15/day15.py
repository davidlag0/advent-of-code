#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 15: Rambunctious Recitation ---

You catch the airport shuttle and try to book a new flight to your vacation island. Due to
the storm, all direct flights have been cancelled, but a route is available to get around
the storm. You take it.

While you wait for your flight, you decide to check in with the Elves back at the North Pole.
They're playing a memory game and are ever so excited to explain the rules!

In this game, the players take turns saying numbers. They begin by taking turns reading from
a list of starting numbers (your puzzle input). Then, each turn consists of considering the
most recently spoken number:

    If that was the first time the number has been spoken, the current player says 0.
    Otherwise, the number had been spoken before; the current player announces how many turns
    apart the number is from when it was previously spoken.

So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the
last number is new) or an age (if the last number is a repeat).

For example, suppose the starting numbers are 0,3,6:

    - Turn 1: The 1st number spoken is a starting number, 0.
    - Turn 2: The 2nd number spoken is a starting number, 3.
    - Turn 3: The 3rd number spoken is a starting number, 6.
    - Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number
      had been spoken, the 4th number spoken is 0.
    - Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before,
      the next number to speak is the difference between the turn number when it was last spoken
      (the previous turn, 4) and the turn number of the time it was most recently spoken before
      then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
    - Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5
      and 2. So, the 6th number spoken is 5 - 2, 3.
    - Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart,
      the 7th number spoken is 1.
    - Turn 8: Since 1 is new, the 8th number spoken is 0.
    - Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference
      between them, 4.
    - Turn 10: 4 is new, so the 10th number spoken is 0.

(The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)

Their question for you is: what will be the 2020th number spoken? In the example above, the
2020th number spoken will be 436.

Here are a few more examples:

    - Given the starting numbers 1,3,2, the 2020th number spoken is 1.
    - Given the starting numbers 2,1,3, the 2020th number spoken is 10.
    - Given the starting numbers 1,2,3, the 2020th number spoken is 27.
    - Given the starting numbers 2,3,1, the 2020th number spoken is 78.
    - Given the starting numbers 3,2,1, the 2020th number spoken is 438.
    - Given the starting numbers 3,1,2, the 2020th number spoken is 1836.

Given your starting numbers, what will be the 2020th number spoken?

--- Part Two ---

Impressed, the Elves issue you a challenge: determine the 30000000th number spoken. For
example, given the same starting numbers as above:

    - Given 0,3,6, the 30000000th number spoken is 175594.
    - Given 1,3,2, the 30000000th number spoken is 2578.
    - Given 2,1,3, the 30000000th number spoken is 3544142.
    - Given 1,2,3, the 30000000th number spoken is 261214.
    - Given 2,3,1, the 30000000th number spoken is 6895259.
    - Given 3,2,1, the 30000000th number spoken is 18.
    - Given 3,1,2, the 30000000th number spoken is 362.

Given your starting numbers, what will be the 30000000th number spoken?
'''

from __future__ import annotations
import os
from typing import NamedTuple, Tuple, List, Dict
import unittest
import time
#import cProfile


TEST_INPUT_FILENAME = 'day_15_test_input.txt'
INPUT_FILENAME = 'day_15_input.txt'


def load_input_file(filename: str) -> List[int]:
    '''Load the input file'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r',
                encoding='utf-8') as input_file:
        return list(map(int, input_file.read().strip().split(',')))


def solve_part1(starting_numbers: List[int], last_turn: int) -> int:
    '''Solve part 1 of the puzzle'''
    turns_dict: Dict[int, List[int]] = dict()
    current_turn: int = 1
    last_spoken_number: int = 0

    if last_turn <= len(starting_numbers):
        return starting_numbers[last_turn - 1]
    else:
        for number in starting_numbers:
            turns_dict[number] = [current_turn]
            current_turn += 1
            last_spoken_number = number

        #performance = cProfile.Profile()
        #performance.enable()
        while current_turn <= last_turn:
            if len(turns_dict[last_spoken_number]) == 1:
                if 0 not in turns_dict:
                    turns_dict[0] = [current_turn]
                else:
                    turns_dict[0].append(current_turn)

                last_spoken_number = 0

            else:
                new_spoken_number = turns_dict[last_spoken_number][-1] - \
                                        turns_dict[last_spoken_number][-2]

                if new_spoken_number not in turns_dict:
                    turns_dict[new_spoken_number] = [current_turn]
                else:
                    turns_dict[new_spoken_number].append(current_turn)

                last_spoken_number = new_spoken_number

            current_turn += 1

        #performance.disable()
        #performance.print_stats()

    return last_spoken_number

class Tests(unittest.TestCase):
    '''Tests'''

    class TestTuple(NamedTuple):
        '''Class to represent a test tuple'''
        turn: int
        spoken_number: int

    class StartingNumberTestTuple(NamedTuple):
        '''Class to represent a starting number test tuple'''
        starting_numbers: List[int]
        last_spoken_number: int

    part1_tests: Tuple[TestTuple, ...] = (
        TestTuple(1, 0),
        TestTuple(2, 3),
        TestTuple(3, 6),
        TestTuple(4, 0),
        TestTuple(5, 3),
        TestTuple(6, 3),
        TestTuple(7, 1),
        TestTuple(8, 0),
        TestTuple(9, 4),
        TestTuple(10, 0),
        TestTuple(2020, 436)
    )

    part1_different_starting_numbers = (
        StartingNumberTestTuple([1, 3, 2], 1),
        StartingNumberTestTuple([2, 1, 3], 10),
        StartingNumberTestTuple([1, 2, 3], 27),
        StartingNumberTestTuple([2, 3, 1], 78),
        StartingNumberTestTuple([3, 2, 1], 438),
        StartingNumberTestTuple([3, 1, 2], 1836),
    )

    part2_different_starting_numbers = (
        StartingNumberTestTuple([0, 3, 6], 175594),
    )

    def test_solve_part1(self) -> None:
        '''Test the solve_part1 function'''
        for case in self.part1_tests:
            with self.subTest(case, i=case[0]):
                self.assertEqual(solve_part1(load_input_file(TEST_INPUT_FILENAME),
                                                case[0]),
                                                case[1])

    def test_solve_part1_with_different_starting_numbers(self) -> None:
        '''Test the solve_part1 function with different starting numbers'''
        for case in self.part1_different_starting_numbers:
            with self.subTest(case, i=case[0]):
                self.assertEqual(solve_part1(case[0], 2020), case[1])

#    def test_solve_part2(self) -> None:
#        '''Test the solve_part1 function for part 2'''
#        for case in self.part2_different_starting_numbers:
#            with self.subTest(case, i=case[0]):
#                self.assertEqual(solve_part1(case[0], 30000000), case[1])


if __name__ == '__main__': # pragma: no cover
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)

    print('Puzzle Answers:')

    part1_start_time = time.perf_counter_ns()
    part1_result = solve_part1(load_input_file(INPUT_FILENAME), 2020)
    part1_stop_time = time.perf_counter_ns()
    print(f'Part 1: {part1_result} - '
        f'Completed in {(part1_stop_time - part1_start_time)/1000}µs')

    #print(f'Part 2: {solve_part1([0, 1, 5, 10, 3, 12, 19], 30000000)}')
