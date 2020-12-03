#!/usr/bin/env python3

# Advent of Code 2020, Day 3
import functools
from operator import mul

def load_grid_information(input_file):
    grid_info = {
        'coordinates': set(),
        'row_length': None,
        'column_length': None,
    }
    row_number = 0
    
    with open(input_file, 'r') as input:
        for line in input:
            char_pos = 0
            
            for char in line.strip():
                if char == '#':
                    grid_info['coordinates'].add((char_pos, row_number))
                
                char_pos += 1
            
            row_number += 1
            
    grid_info['row_length'] = char_pos
    grid_info['column_length'] = row_number

    return grid_info

def get_number_of_trees(slope):
    number_of_trees = 0
    
    for y in range(1, grid['column_length']):
        x = slope * y
        
        if x >= grid['row_length']:
            x_tile = x % grid['row_length']
        else:
            x_tile = x
        
        if (x_tile, y) in grid['coordinates']:
            number_of_trees += 1
            
    return number_of_trees

if __name__ == '__main__':
    grid = load_grid_information('day_3_input')

    # Part 1
    print(f'Part 1: {get_number_of_trees(3)}')

    # Part 2
    print(f'Part 2: {functools.reduce(mul, [get_number_of_trees(slope) for slope in [1, 3, 5, 7, 1/2]], 1)}')
    