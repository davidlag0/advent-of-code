#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 14: Docking Data ---

As your ferry approaches the sea port, the captain asks for your help again. The computer system
that runs this port isn't compatible with the docking program on the ferry, so the docking
parameters aren't being correctly initialized in the docking program's memory.

After a brief inspection, you discover that the sea port's computer system uses a strange
bitmask system in its initialization program. Although you don't have the correct decoder
chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a value
to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring
bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

The bitmask is always given as a string of 36 bits, written with the most significant
bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on
the right. The current bitmask is applied to values immediately before they are written to
memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the
value unchanged.

For example, consider the following program:

mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0

This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite
two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten
with 1.

The program then attempts to write the value 11 to memory address 8. By expanding everything
out to individual bits, the mask is applied as follows:

value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)

So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program
tries to write 101 to address 7:

value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)

This time, the mask has no effect, as the bits it overwrote were already the values the mask
tried to set. Finally, the program tries to write 0 to address 8:

value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)

64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in memory after
the initialization program completes. (The entire 36-bit address space begins initialized to
the value 0 at every address.) In the above example, only two values in memory are not
zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.

Execute the initialization program. What is the sum of all values left in memory after it
completes? (Do not truncate the sum to 36 bits.)
'''

from __future__ import annotations
import os
from typing import Iterable, Dict
import unittest
import re


TEST_INPUT_FILENAME = 'day_14_test_input.txt'
INPUT_FILENAME = 'day_14_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input_file:
        return map(str.strip, input_file.readlines())


class Program:
    '''Class that represents a program'''
    mask_pattern = re.compile(r'mask\s=\s([X01]{36})')
    memwrite_pattern = re.compile(r'mem\[(\d+)\]\s=\s(\d+)')

    def __init__(self) -> None:
        self.__mask = 'X' * 36
        self.__memory: Dict[int, int] = dict()

    def read_program(self, instruction: str) -> None:
        '''Read a program line and call the proper action to be executed'''
        if match := re.match(self.mask_pattern, instruction):
            self.__mask = match.group(1)
        if match := re.match(self.memwrite_pattern, instruction):
            value = int(match.group(2)) | int(self.mask.replace('X', '0'), 2)
            value = value & int(self.mask.replace('X', '1'), 2)
            self.set_memory(int(match.group(1)), value)

    @property
    def mask(self) -> str:
        '''Getter for mask class member'''
        return self.__mask

    @mask.setter
    def mask(self, value: str) -> None:
        self.__mask = value

    def get_memory(self, memslot: int) -> int:
        '''Getter for memory class member'''
        return self.__memory[memslot]

    def set_memory(self, memslot: int, value: int) -> None:
        '''Setter for memory class member'''
        self.__memory[memslot] = value

    def dump_memory(self) -> Dict[int, int]:
        '''Return the full memory dump of the program'''
        return self.__memory


class Tests(unittest.TestCase):
    '''Tests'''

    mask_instruction = 'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
    memwrite_instruction = 'mem[8] = 11'
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
    memory_changes = (
        ('mem[8] = 11', 8, 73),
        ('mem[7] = 101', 7, 101),
        ('mem[8] = 0', 8, 64)
    )

    def test_set_mask(self) -> None:
        '''Test the mask setter of the Program class'''

        program = Program()
        program.mask = self.mask
        self.assertEqual(program.mask, self.mask)

    def test_read_program_with_mask(self) -> None:
        '''Test the read_program function with a mask instruction'''

        program = Program()
        program.read_program(self.mask_instruction)
        self.assertEqual(program.mask, self.mask)

    def test_read_program_with_memwrite_and_all_x_mask(self) -> None:
        '''Test the read_program function with a memwrite instruction and all X mask'''

        program = Program()
        program.read_program(self.memwrite_instruction)
        self.assertEqual(program.get_memory(8), 11)

    def test_read_program_with_memwrites_and_mask(self) -> None:
        '''Test the read_program function with memwrite instructions and a specific mask'''

        program = Program()
        program.read_program(self.mask_instruction)

        for case in self.memory_changes:
            with self.subTest(case):
                program.read_program(case[0])
                self.assertEqual(program.get_memory(case[1]), case[2])

    def test_solve_part1_with_test_data(self) -> None:
        '''Test the solve_part1 function with test data'''
        self.assertEqual(solve_part1(TEST_INPUT_FILENAME), 165)


def solve_part1(filename: str) -> int:
    '''Solve part 1 of the puzzle'''
    program = Program()
    for instruction in load_input_file(filename):
        program.read_program(instruction)
    return sum(program.dump_memory().values())


if __name__ == '__main__': # pragma: no cover
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f'Part 1: {solve_part1(INPUT_FILENAME)}')
    print(f'Part 2: {0}')
