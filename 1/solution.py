#! /usr/bin/env python3
import os
from functools import reduce

TEST_FILE_1 = f'{os.path.dirname(__file__)}/test_input_1'
TEST_FILE_2 = f'{os.path.dirname(__file__)}/test_input_2'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def first_and_last_digit(line):
  digits = [char for char in line if char in '1234567890']
  return int(f'{digits[0]}{digits[-1]}')
 
def part_1(file):
  with open(file) as input:
    calibrations_numbers = [first_and_last_digit(line.strip()) for line in input.readlines()]
    return sum(calibrations_numbers)

# Solution
print(part_1(INPUT_FILE))

# Tests
assert part_1(TEST_FILE_1) == 142