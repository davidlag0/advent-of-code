#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 10: Adapter Array ---
Patched into the aircraft's data port, you discover weather forecasts of a massive tropical storm.
Before you can figure out whether it will impact your vacation plans, however, your device suddenly
turns off!

Its battery is dead.

You'll need to plug it in. There's only one problem: the charging outlet near your seat produces
the wrong number of jolts. Always prepared, you make a list of all of the joltage adapters in your
bag.

Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given
adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output
joltage.

In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the
highest-rated adapter in your bag. (If your adapter list were 3, 9, and 6, your device's built-in
adapter would be rated for 12 jolts.)

Treat the charging outlet near your seat as having an effective joltage rating of 0.

Since you have some time to kill, you might as well test all of your adapters. Wouldn't want to get
to your resort and realize you can't even charge your device!

If you use every adapter in your bag at once, what is the distribution of joltage differences
between the charging outlet, the adapters, and your device?

For example, suppose that in your bag, you have adapters with the following joltage ratings:

16
10
15
5
1
11
7
19
6
12
4
With these adapters, your device's built-in joltage adapter would be rated for 19 + 3 = 22 jolts,
3 higher than the highest-rated adapter.

Because adapters can only connect to a source 1-3 jolts lower than its rating, in order to use
every adapter, you'd need to choose them like this:

The charging outlet has an effective rating of 0 jolts, so the only adapters that could connect
to it directly would need to have a joltage rating of 1, 2, or 3 jolts. Of these, only one you
have is an adapter rated 1 jolt (difference of 1).
From your 1-jolt rated adapter, the only choice is your 4-jolt rated adapter (difference of 3).
From the 4-jolt rated adapter, the adapters rated 5, 6, or 7 are valid choices. However, in order
to not skip any adapters, you have to pick the adapter rated 5 jolts (difference of 1).
Similarly, the next choices would need to be the adapter rated 6 and then the adapter rated 7 (with
difference of 1 and 1).
The only adapter that works with the 7-jolt rated adapter is the one rated 10 jolts (difference of
3).
From 10, the choices are 11 or 12; choose 11 (difference of 1) and then 12 (difference of 1).
After 12, only valid adapter has a rating of 15 (difference of 3), then 16 (difference of 1), then
19 (difference of 3).
Finally, your device's built-in adapter is always 3 higher than the highest adapter, so its rating
is 22 jolts (always a difference of 3).
In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of
3 jolts.

Here is a larger example:

28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
In this larger example, in a chain that uses all of the adapters, there are 22 differences of 1
jolt and 10 differences of 3 jolts.

Find a chain that uses all of your adapters to connect the charging outlet to your device's
built-in adapter and count the joltage differences between the charging outlet, the adapters, and
your device. What is the number of 1-jolt differences multiplied by the number of 3-jolt
differences?

--- Part Two ---
To completely determine whether you have enough adapters, you'll need to figure out how many
different ways they can be arranged. Every arrangement needs to connect the charging outlet to
your device. The previous rules about when adapters can successfully connect still apply.

The first example above (the one that starts with 16, 10, 15) supports the following arrangements:

(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
(The charging outlet and your device's built-in adapter are shown in parentheses.) Given the
adapters from the first example, the total number of arrangements that connect the charging
outlet to your device is 8.

The second example above (the one that starts with 28, 33, 18) has many arrangements. Here are a
few:

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)

(0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
46, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
46, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
47, 48, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
47, 49, (52)

(0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
48, 49, (52)
In total, this set of adapters can connect the charging outlet to your device in 19208 distinct
arrangements.

You glance back down at your bag and try to remember why you brought so many adapters; there must
be more than a trillion valid ways to arrange them! Surely, there must be an efficient way to count
the arrangements.

What is the total number of distinct ways you can arrange the adapters to connect the charging
outlet to your device?
'''

import os
from typing import Iterable, Tuple, TypedDict, List, Set
from itertools import combinations
from functools import reduce
from operator import mul
import unittest


class JoltageSets(TypedDict):
    '''Typing for joltage sets'''
    prev: int
    set: Set[int]
    next: int
    combinations: List[Set[int]]


TEST_1_INPUT_FILENAME = 'day_10_small_input_1.txt'
TEST_2_INPUT_FILENAME = 'day_10_small_input_2.txt'
INPUT_FILENAME = 'day_10_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file.'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input_file:
        return map(str.strip, input_file.readlines())


def find_joltage_differences(filename: str) -> Tuple[int, int]:
    '''Find the number of 3-jolt and 1-jolt differences.'''
    differences_of_1_jolt = 0
    differences_of_3_jolts = 0
    current_joltage = 0

    joltages = sorted(tuple(map(int, load_input_file(filename))))

    for joltage in joltages:
        if (current_joltage + 1) == joltage:
            differences_of_1_jolt += 1
        elif (current_joltage + 3) == joltage:
            differences_of_3_jolts += 1

        current_joltage = joltage

    return (differences_of_1_jolt, differences_of_3_jolts + 1)


def length_of_valid_joltage_combinations(joltage_sets: List[JoltageSets]) -> int:
    '''
    Filter the joltage combinations and return the product of the list of length of
    the remaining groups of combinations
    '''
    length_of_combinations = []

    for joltage_set in joltage_sets:
        filtered_joltage_combinations = []

        for length in range(1, len(joltage_set) + 1):

            joltage_set_combinations = combinations(joltage_set['set'], length)

            for joltage_set_combination in joltage_set_combinations:
                if (min(joltage_set_combination) - joltage_set['prev'] <= 3) and \
                    (joltage_set['next'] - max(joltage_set_combination) <= 3):
                    filtered_joltage_combinations.append(joltage_set_combination)

        length_of_combinations.append(len(filtered_joltage_combinations))

    return reduce(mul, length_of_combinations, 1)


def calculate_distinct_ways(filename: str) -> int:
    '''
    Calculate the number of distinct ways to connect adapters together
    '''
    position = 0
    joltage_sets: List[JoltageSets] = []
    current_set = set()

    joltages = sorted(tuple(map(int, load_input_file(filename))))
    joltages = [0, *joltages, max(joltages) + 3]

    for position in range(1, len(joltages)):
        try:
            if (joltages[position + 1] - joltages[position]) < 3:
                current_set.add(joltages[position])
                current_set.add(joltages[position + 1])
            else:
                if len(current_set) >= 2:
                    joltage_sets.append({
                                        'prev': joltages[joltages.index(min(current_set)) - 1],
                                        'set': current_set,
                                        'next': joltages[position + 1],
                                        'combinations': [],
                                        })
                current_set = set()

        except IndexError:
            pass

    return length_of_valid_joltage_combinations(joltage_sets)


class Tests(unittest.TestCase):
    '''Tests'''

    def test_find_joltage_differences_1(self) -> None:
        '''Test for the joltage differences found.'''
        result = find_joltage_differences(TEST_1_INPUT_FILENAME)
        self.assertEqual(result, (7, 5))

    def test_find_joltage_differences_2(self) -> None:
        '''Test for the joltage differences found.'''
        result = find_joltage_differences(TEST_2_INPUT_FILENAME)
        self.assertEqual(result, (22, 10))

    def test_calculate_distinct_ways_1(self) -> None:
        '''Test for the calculation of distinct ways to connect adapters.'''
        result = calculate_distinct_ways(TEST_1_INPUT_FILENAME)
        self.assertEqual(result, 8)

    def test_calculate_distinct_ways_2(self) -> None:
        '''Test for the calculation of distinct ways to connect adapters.'''
        result = calculate_distinct_ways(TEST_2_INPUT_FILENAME)
        self.assertEqual(result, 19208)


if __name__ == '__main__': # pragma: no cover
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    (diff1, diff3) = find_joltage_differences(INPUT_FILENAME)
    print(f"Part 1: {diff1 * diff3}")
    print(f"Part 2: {calculate_distinct_ways(INPUT_FILENAME)}")
