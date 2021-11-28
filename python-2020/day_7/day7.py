#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
'''

import os
import re
from typing import Iterable
import unittest


TEST_INPUT_FILENAME = 'day_7_small_input.txt'
INPUT_FILENAME = 'day_7_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input:
        return map(str.strip, input.readlines())
    

def build_bag_tree(outer_bags: Iterable[str]) -> dict:
    all_bags = {}
    bag_list_pattern = re.compile(r'\d+\s(\w+\s\w+)\sbag')

    for bag in outer_bags:
        outer_bag, inside_bags_list = bag.split(' bags contain ')
        all_bags[outer_bag] = set(bag_list_pattern.findall(inside_bags_list))
    
    return all_bags


def traverse_bag_tree(bag_tree: dict, current_bag: set, searched_bag_name: str) -> bool:
    if searched_bag_name in bag_tree[current_bag]:
        return True

    if len(bag_tree[current_bag]) == 0:
        return False
    
    return any(traverse_bag_tree(bag_tree, bag, searched_bag_name) for bag in bag_tree[current_bag])


def count_bag_containers(outer_bags: Iterable[str], bag_name: str) -> int:
    bag_count = 0
    bag_tree = build_bag_tree(outer_bags)

    for bag in bag_tree.keys():
        if traverse_bag_tree(bag_tree, bag, bag_name):
            bag_count += 1
        
    return bag_count


def get_match_dict(match):
    return {match[1]: int(match[0])}


def build_bag_tree_with_count(outer_bags: Iterable[str]) -> dict:
    all_bags = {}
    bag_list_pattern = re.compile(r'(\d)+\s(\w+\s\w+)\sbag')

    for bag in outer_bags:
        outer_bag, inside_bags_list = bag.split(' bags contain ')
        for match in bag_list_pattern.findall(inside_bags_list):
            if outer_bag in all_bags:
                all_bags[outer_bag].update(get_match_dict(match))
            else:
                all_bags[outer_bag] = get_match_dict(match)
    
    return all_bags


def traverse_bag_tree_and_count(bag_tree: dict, bag_name: str) -> int:
    if bag_name not in bag_tree:
        return 0
    
    return sum(bag_tree[bag_name].values()) + sum(bag_tree[bag_name][bag] * traverse_bag_tree_and_count(bag_tree, bag) for bag in bag_tree[bag_name])


def count_individual_bags(outer_bags: Iterable[str], bag_name: str) -> int:
    bag_tree = build_bag_tree_with_count(outer_bags)
    
    return traverse_bag_tree_and_count(bag_tree, bag_name)


class Tests(unittest.TestCase):
    
    def test_count_bag_containers(self):
        cases = (
            ('light red', 0),
            ('dark orange', 0),
            ('bright white', 2),
            ('muted yellow', 2),
            ('shiny gold', 4),
            ('faded blue', 7),
            ('vibrant plum', 5),
            ('dotted black', 7),
            ('dark olive', 5),
        )
        
        for bag_name, expected in cases:
            with self.subTest(bag_name):
                result = count_bag_containers(load_input_file(TEST_INPUT_FILENAME), bag_name)
                self.assertEqual(result, expected)

    def test_count_gold_bag_containers(self):
        result = count_bag_containers(load_input_file(TEST_INPUT_FILENAME), 'shiny gold')
        self.assertEqual(result, 4)
    
    def test_count_individual_bags(self):
        cases = (
            ('faded blue', 0),
            ('dotted black', 0),
            ('vibrant plum', 11),
            ('dark olive', 7),
            ('shiny gold', 32),
        )
        
        for bag_name, expected in cases:
            with self.subTest(bag_name):
                result = count_individual_bags(load_input_file(TEST_INPUT_FILENAME), bag_name)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f"Part 1: {count_bag_containers(load_input_file(INPUT_FILENAME), 'shiny gold')}")
    print(f"Part 2: {count_individual_bags(load_input_file(INPUT_FILENAME), 'shiny gold')}")
