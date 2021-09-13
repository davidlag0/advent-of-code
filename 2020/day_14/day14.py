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

--- Part Two ---

For some reason, the sea port's computer system still can't communicate with your ferry's
docking program. It must be using version 2 of the decoder chip!

A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts
as a memory address decoder. Immediately before a value is written to memory, each bit in
the bitmask modifies the corresponding bit of the destination memory address in the following
way:

    If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating.

A floating bit is not connected to anything and instead fluctuates unpredictably. In practice,
this means the floating bits will take on all possible values, potentially causing many memory
addresses to be written all at once!

For example, consider the following program:

mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1

When this program goes to write to memory address 42, it first applies the bitmask:

address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X

After applying the mask, four bits are overwritten, three of which are different, and two of
which are floating. Floating bits take on every possible combination of values; with two
floating bits, four actual memory addresses are written:

000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)

Next, the program is about to write to memory address 26 with a different bitmask:

address: 000000000000000000000000000000011010  (decimal 26)
mask:    00000000000000000000000000000000X0XX
result:  00000000000000000000000000000001X0XX

This results in an address with three floating bits, causing writes to eight memory addresses:

000000000000000000000000000000010000  (decimal 16)
000000000000000000000000000000010001  (decimal 17)
000000000000000000000000000000010010  (decimal 18)
000000000000000000000000000000010011  (decimal 19)
000000000000000000000000000000011000  (decimal 24)
000000000000000000000000000000011001  (decimal 25)
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)

The entire 36-bit address space still begins initialized to the value 0 at every address, and
you still need the sum of all values left in memory at the end of the program. In this example,
the sum is 208.

Execute the initialization program using an emulator for a version 2 decoder chip. What is the
sum of all values left in memory after it completes?
'''

from __future__ import annotations
import os
from typing import Iterable, Dict, List, Iterator, Match
import unittest
import re
import math


TEST_INPUT_FILENAME = 'day_14_test_input.txt'
TEST_INPUT_FILENAME2 = 'day_14_test_input2.txt'
INPUT_FILENAME = 'day_14_input.txt'


def load_input_file(filename: str) -> Iterable[str]:
    '''Load the input file'''
    with open(os.path.join(os.path.dirname(__file__), filename), 'r',
                encoding='utf-8') as input_file:
        return map(str.strip, input_file.readlines())


class Program:
    '''Class that represents a program'''
    mask_pattern = re.compile(r'mask\s=\s([X01]{36})')
    memwrite_pattern = re.compile(r'mem\[(\d+)\]\s=\s(\d+)')

    def __init__(self, version_one: bool = True) -> None:
        self.__mask = 'X' * 36
        self.__memory: Dict[int, int] = {}
        self.__version_one = version_one

    def apply_v2_mask(self, memory_slot: int) -> str:
        '''Return a masked address'''
        result_address: str = ''

        for (address_char, mask_char) in zip('{:36b}'.format(memory_slot), self.mask):
            if address_char == '1' and mask_char == '0':
                result_address += '1'
            else:
                result_address += mask_char

        return result_address

    @staticmethod
    def resolve_address(masked_address: str) -> List[int]:
        '''Given a masked address, return memory addresses ready for writing'''
        addresses: List[int] = []
        number_of_x: int = masked_address.count('X')
        number_of_addresses = int(math.pow(2, number_of_x))

        for specific_address in range(number_of_addresses):
            binary_address: str = '{0:b}'.format(specific_address).zfill(number_of_x)
            address_iterator: Iterator[str] = iter(binary_address)

            # pylint: disable=unused-argument
            def replace(match: Match[str]) -> str:
                # pylint: disable=cell-var-from-loop
                return next(address_iterator)

            addresses.append(int(re.sub('X', replace, masked_address), 2))

        return addresses

    def read_program(self, instruction: str) -> None:
        '''Read a program line and call the proper action to be executed'''
        if match := re.match(self.mask_pattern, instruction):
            self.__mask = match.group(1)
        if match := re.match(self.memwrite_pattern, instruction):
            if self.version_one:
                value = int(match.group(2)) | int(self.mask.replace('X', '0'), 2)
                value = value & int(self.mask.replace('X', '1'), 2)
                self.set_memory(int(match.group(1)), value)
            else:
                for mem_address in self.resolve_address(self.apply_v2_mask(int(match.group(1)))):
                    self.set_memory(mem_address, int(match.group(2)))

    @property
    def mask(self) -> str:
        '''Getter for mask class member'''
        return self.__mask

    @mask.setter
    def mask(self, value: str) -> None:
        self.__mask = value

    @property
    def version_one(self) -> bool:
        '''Getter for version_one class member'''
        return self.__version_one

#    @version_one.setter
#    def version_one(self, value: bool) -> None:
#        self.__version_one = value

    def get_memory(self, memslot: int) -> int:
        '''Getter for memory class member'''
        return self.__memory[memslot]

    def set_memory(self, memslot: int, value: int) -> None:
        '''Setter for memory class member'''
        self.__memory[memslot] = value

    def dump_memory(self) -> Dict[int, int]:
        '''Return the full memory dump of the program'''
        return self.__memory


def solve(filename: str, version_one: bool = True) -> int:
    '''Solve part 1 of the puzzle'''
    program = Program(version_one=version_one)
    for instruction in load_input_file(filename):
        program.read_program(instruction)
    return sum(program.dump_memory().values())

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
    part2_tests = (
        (
            'mask = 000000000000000000000000000000X1001X',
            42,
            '000000000000000000000000000000X1101X',
            [26, 27, 58, 59],
            'mem[42] = 100',
            400
        ),
        (
            'mask = 00000000000000000000000000000000X0XX',
            26,
            '00000000000000000000000000000001X0XX',
            [16, 17, 18, 19, 24, 25, 26, 27],
            'mem[26] = 1',
            8
        )
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
        self.assertEqual(solve(TEST_INPUT_FILENAME, version_one=True), 165)

    def test_apply_v2_mask(self) -> None:
        '''Test the apply_v2_mask function'''

        program = Program()

        for case in self.part2_tests:
            with self.subTest(case):
                program.read_program(case[0])
                self.assertEqual(program.apply_v2_mask(case[1]), case[2])

    def test_resolve_address(self) -> None:
        '''Test the resolve_address function'''

        program = Program()

        for case in self.part2_tests:
            with self.subTest(case):
                self.assertListEqual(program.resolve_address(case[2]), case[3])

    def test_v2_read_program(self) -> None:
        '''Test the read_program function for version_one = False'''

        for case in self.part2_tests:
            program = Program(version_one=False)

            with self.subTest(case):
                program.read_program(case[0])
                program.read_program(case[4])
                self.assertEqual(sum(program.dump_memory().values()), case[5])

    def test_solve_part2_with_test_data(self) -> None:
        '''Test the solve_part1 function with test data'''
        self.assertEqual(solve(TEST_INPUT_FILENAME2, version_one=False), 208)


if __name__ == '__main__': # pragma: no cover
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f'Part 1: {solve(INPUT_FILENAME, version_one=True)}')
    print(f'Part 2: {solve(INPUT_FILENAME, version_one=False)}')
