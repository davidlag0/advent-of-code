#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 9: Encoding Error ---
With your neighbor happily enjoying their video game, you turn your attention to an open data
port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer through the clever use
of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which,
conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should
be the sum of any two of the 25 immediately previous numbers. The two numbers will have different
values, and there might be more than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be
valid, the next number must be the sum of two of those numbers:

26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
49 would be a valid next number, as it is the sum of 24 and 25.
100 would not be valid; no two of the previous 25 numbers sum to 100.
50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the
pair must be different. Suppose the 26th number is 45, and the first number (no longer an option,
as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be
some pair of numbers among 1-19, 21-25, or 45 that add up to it:

26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
65 would not be valid, as no two of the available numbers sum to it.
64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and has a preamble of
length 5):

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this example, after the 5-number preamble, almost every number is the sum of two of the
previous 5 numbers; the only number that does not follow this rule is 127.

The first step of attacking the weakness in the XMAS data is to find the first number in the
list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the
first number that does not have this property?

--- Part Two ---
The final step in breaking the XMAS encryption relies on the invalid number you just found: you
must find a contiguous set of at least two numbers in your list which sum to the invalid number
from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this list, adding up all of the numbers from 15 through 40 produces the invalid number from
step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous
range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?
'''

import os
from typing import Iterable
from itertools import combinations
import unittest


TEST_INPUT_FILENAME = 'day_9_small_input.txt'
INPUT_FILENAME = 'day_9_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file.'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input_file:
        return map(str.strip, input_file.readlines())


def find_encoding_error(filename: str, preamble_length: int) -> int:
    '''Find the number causing the encoding error.'''
    numbers = tuple(map(int, load_input_file(filename)))

    for position in range(preamble_length, len(numbers)):
        preamble = numbers[position - preamble_length:position]
        preamble_sums = set(map(sum, combinations(preamble, 2)))

        if numbers[position] not in preamble_sums:
            return numbers[position]


def find_encryption_weakness(filename: str, invalid_number: int) -> int:
    '''Find the suite of contiguous numbers causing the encryption weakness.'''
    numbers = tuple(map(int, load_input_file(filename)))

    for length_of_contiguous_numbers in range(2, len(numbers)):
        for position in range(0, len(numbers) - length_of_contiguous_numbers):
            contiguous_numbers = numbers[position:position + length_of_contiguous_numbers]
            if sum(contiguous_numbers) == invalid_number:
                return max(contiguous_numbers) + min(contiguous_numbers)


class Tests(unittest.TestCase):
    '''Tests'''

    # The global test setup is not used here but could be used for upcoming AoC
    # puzzles as required. I couldn't find how to get this working previously and
    # now it works so keeping it as a reference.
    test_numbers = None

    @classmethod
    def setUpClass(cls):
        cls.test_numbers = [number for number in load_input_file(TEST_INPUT_FILENAME)]

    @classmethod
    def tearDownClass(cls):
        cls.test_numbers = None

    def test_find_encoding_error(self):
        '''Test to find the encoding error.'''
        result = find_encoding_error(TEST_INPUT_FILENAME, 5)
        self.assertEqual(result, 127)

    def test_encryption_weakness(self):
        '''Test to find the encryption weakness'''
        result = find_encryption_weakness(TEST_INPUT_FILENAME, 127)
        self.assertEqual(result, 62)


if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f"Part 1: {find_encoding_error(INPUT_FILENAME, 25)}")
    print(f"Part 2: {find_encryption_weakness(INPUT_FILENAME, 22477624)}")
