#!/usr/bin/env python3

# Advent of Code 2020, Day 2
import re

password_rules = []
rule_pattern = re.compile(r'(\d+)\-(\d+)\s(\w)\:\s(\w+)')

with open('day_2_input', 'r') as input:
    for line in input:
        password_rules.append(re.findall(rule_pattern, line.strip())[0])

# To show the rules to help for debug.
# print(f'Rules: {password_rules}')

# Part 1
# string.count() method may be more common.
valid_passwords = sum([1 for min, max, char, password in password_rules if int(min) <= len(re.findall(r'' + char, password)) <= int(max)])
print(f'Part 1: {str(valid_passwords)}')

# Part 2
valid_passwords = 0

for min, max, char, password in password_rules:
    matches = 0
    
    for match in re.finditer(r'' + char, password):
        if match.span()[1] in (int(min), int(max)):
            matches += 1
    
    if matches == 1:
        valid_passwords += 1

print(f'Part 2: {str(valid_passwords)}')
