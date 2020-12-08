#!/usr/bin/env python3

# Advent of Code 2020
'''
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

--- Part Two ---
After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6
After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
'''

import os
import re
from typing import Iterable
import unittest


TEST_INPUT_FILENAME = 'day_8_small_input.txt'
INPUT_FILENAME = 'day_8_input.txt'
INSTRUCTION_PATTERN = re.compile(r'(nop|acc|jmp)\s(.\d+)')


def load_input_file(filename: str) -> Iterable[str]:
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as input:
        return map(str.strip, input.readlines())


def load_instructions(filename: str) -> list:
    instructions = []

    for line in load_input_file(filename):
        instructions.append(line)
        
    return instructions


def decode_instruction(instruction) -> tuple:
    decoded_instruction = INSTRUCTION_PATTERN.findall(instruction)
    return (decoded_instruction[0][0], int(decoded_instruction[0][1]))


def decode_all_instructions(instruction_list: list) -> list:
    decoded_instructions = []
    
    for instruction in instruction_list:
        decoded_instructions.append(decode_instruction(instruction))

    return decoded_instructions


def execute_instruction(instruction: tuple, initial_pointer: int = 0, accumulator: int = 0, decoded: bool = False) -> tuple:
    current_pointer = initial_pointer
    current_accumulator = accumulator
    
    if decoded:
        keyword, value = instruction
    else:
        keyword, value = decode_instruction(instruction)
    
    if keyword == 'acc':
        current_accumulator += value

    if keyword == 'jmp':
        current_pointer += value
    else:
        current_pointer += 1
    
    return (current_pointer, current_accumulator)


def execute_program(instruction_list: list, decoded: bool = False) -> tuple:
    pointer, accumulator = 0, 0
    executed_lines = set()
    status = 'success'

    while True:
        if pointer >= len(instruction_list):
            break
        
        if pointer not in executed_lines:
            executed_lines.add(pointer)
            pointer, accumulator = execute_instruction(instruction_list[pointer], pointer, accumulator, decoded=decoded)
        else:
            status = 'aborted'
            break
        
    return (accumulator, status)


def execute_program_after_instruction_change(filename: str) -> tuple:
    decoded_instruction_list = decode_all_instructions(load_instructions(filename))
    #print(f'length: {len(decoded_instruction_list)}')
    
    for pointer in range(0, len(decoded_instruction_list)):
        fixed_decoded_instruction_list = decoded_instruction_list.copy()
        
        if decoded_instruction_list[pointer][0] == 'jmp':
            fixed_decoded_instruction_list[pointer] = ('nop', fixed_decoded_instruction_list[pointer][1])
        elif decoded_instruction_list[pointer][0] == 'nop':
            fixed_decoded_instruction_list[pointer] = ('jmp', fixed_decoded_instruction_list[pointer][1])
        
        #print(f'new instructions: {fixed_decoded_instruction_list}')
        #print(f'pointer: {pointer}')
        result = execute_program(fixed_decoded_instruction_list, decoded=True)
        
        if result[1] == 'success':
            break
    
    return result


class Tests(unittest.TestCase):
    
    test_instructions = [
        ('nop +0', ('nop', 0), (1, 0), (0, 'aborted')),
        ('acc +1', ('acc', 1), (1, 1), (5, 'aborted')),
        ('jmp +4', ('jmp', 4), (4, 0), (4, 'aborted')),
        ('acc +3', ('acc', 3), (1, 3), (5, 'aborted')),
        ('jmp -3', ('jmp', -3), (-3, 0), (-94, 'aborted')),
        ('acc -99', ('acc', -99), (1, -99), (5, 'aborted')),
        ('acc +1', ('acc', 1), (1, 1), (5, 'aborted')),
        ('jmp -4', ('jmp', -4), (-4, 0), (8, 'success')),
        ('acc +6', ('acc', 6), (1, 6), (5, 'aborted')),
    ]
    
    def test_load_instructions(self):
        result = load_instructions(TEST_INPUT_FILENAME)
        self.assertEqual(result, [instruction[0] for instruction in self.test_instructions])
    
    def test_decode_instructions(self):
        for instruction in self.test_instructions:
            with self.subTest(instruction[0]):
                result = decode_instruction(instruction[0])
                self.assertEqual(result, instruction[1])

    def test_execute_instructions(self):
        for instruction in self.test_instructions:
            with self.subTest(instruction[0]):
                result = execute_instruction(instruction[0], 0, 0)
                self.assertEqual(result, instruction[2])
                
    def test_execute_program(self):
        result = execute_program(load_instructions(TEST_INPUT_FILENAME))
        self.assertEqual(result, (5, 'aborted'))
        
    def test_execute_program_after_instruction_change(self):
        result = execute_program_after_instruction_change(TEST_INPUT_FILENAME)
        self.assertEqual(result, (8, 'success'))


if __name__ == '__main__':
    print('Running unit tests...')
    unittest.main(verbosity=2, exit=False)
    print('Puzzle Answers:')
    print(f"Part 1: {execute_program(load_instructions(INPUT_FILENAME))[0]}")
    print(f"Part 2: {execute_program_after_instruction_change(INPUT_FILENAME)[0]}")
