#!/usr/bin/env python3

from itertools import combinations

# Advent of Code 2020, Day 1
amounts = []

with open('day_1_input', 'r') as input:
    for line in input:
        amounts.append(int(line))
    
answer1 = [(x * y) for (x, y) in combinations(amounts, 2) if (x + y) == 2020]
print(f'Part 1: {answer1[0]}')

answer2 = [(x * y * z) for (x, y, z) in combinations(amounts, 3) if (x + y + z) == 2020]
print(f'Part 2: {answer2[0]}')
