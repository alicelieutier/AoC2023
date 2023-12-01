#! /usr/bin/env python3
import os
import regex as re
from functools import reduce

TEST_FILE_1 = f'{os.path.dirname(__file__)}/test_input_1'
TEST_FILE_2 = f'{os.path.dirname(__file__)}/test_input_2'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def first_and_last_digit(line):
  digits = [int(char) for char in line if char in '1234567890']
  return digits[0], digits[-1]

DIGIT_NAMES = {
  'one' : 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9
}

def to_digit(digit_or_name_str):
  if digit_or_name_str in DIGIT_NAMES:
    return DIGIT_NAMES[digit_or_name_str]
  return int(digit_or_name_str)

def real_first_and_last_digit(line):
  digit_strings = re.findall(r'[0-9]|one|two|three|four|five|six|seven|eight|nine', line, overlapped=True)
  first = to_digit(digit_strings[0])
  last = to_digit(digit_strings[-1])
  return first, last

def calibration_value(digits):
  first, last = digits
  return first * 10 + last

def part_1(file):
  with open(file) as input:
    values = [calibration_value(first_and_last_digit(line.strip())) for line in input.readlines()]
    return sum(values)
   
def part_2(file):
  with open(file) as input:
    values = [calibration_value(real_first_and_last_digit(line.strip())) for line in input.readlines()]
    return sum(values)

# Solution
print(part_1(INPUT_FILE)) # 54951
print(part_2(INPUT_FILE)) # 55218

# Tests
assert part_1(TEST_FILE_1) == 142
assert part_2(TEST_FILE_2) == 281

assert real_first_and_last_digit('onenine78nifgj') == (1,8)
assert real_first_and_last_digit('mjqhmqnbhjtbxkrsrppeight2dctpspsix58') == (8,8)
assert real_first_and_last_digit('4twonelc') == (4,1)
