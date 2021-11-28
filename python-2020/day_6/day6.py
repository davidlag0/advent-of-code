#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 6: Custom Customs ---
As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.

The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.

However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:

abcx
abcy
abcz
In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)

Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers are on a single line. For example:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

The first group contains one person who answered "yes" to 3 questions: a, b, and c.
The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
The last group contains one person who answered "yes" to only 1 question, b.
In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

--- Part Two ---
As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

Using the same example as above:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
In the second group, there is no question to which everyone answered "yes".
In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
In the fourth group, everyone answered yes to only 1 question, a.
In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
'''
import os
from typing import Iterable
import unittest

def load_input_file(filename: str) -> Iterable[str]:
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input:
        return map(str.strip, input.readlines())

def count_unique_group_answers(group_answers: Iterable[str]) -> int:
    total_answers = 0
    current_group_answers = set()
    
    for participant_answers in group_answers:
        if len(participant_answers) > 0:
            for answer in participant_answers:
                current_group_answers.add(answer)
        else:
            total_answers += len(current_group_answers)
            current_group_answers = set()
            
    # Required for the last group answers as we cannot know in advance whether the current
    # line is the last or not.
    total_answers += len(current_group_answers)
            
    return total_answers

def count_common_group_answers(group_answers: Iterable[str]) -> int:
    total_answers = 0
    current_group_answers = []
    
    for participant_answers in group_answers:
        if len(participant_answers) > 0:
            current_group_answers.append(set(participant_answers))
        else:
            total_answers += len(set.intersection(*current_group_answers))
            current_group_answers = []
            
    # Required for the last group answers as we cannot know in advance whether the current
    # line is the last or not.
    total_answers += len(set.intersection(*current_group_answers))
    
    return total_answers

class Tests(unittest.TestCase):
    def test_count_unique_group_answers(self):
        result = count_unique_group_answers(load_input_file('day_6_small_input.txt'))
        self.assertEqual(result, 11)
        
    def test_count_common_group_answers(self):
        result = count_common_group_answers(load_input_file('day_6_small_input.txt'))
        self.assertEqual(result, 6)

if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f'Part 1: {count_unique_group_answers(load_input_file("day_6_input.txt"))}')
    print(f'Part 2: {count_common_group_answers(load_input_file("day_6_input.txt"))}')
