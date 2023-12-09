#! /usr/bin/env python3
import os
import re
from itertools import pairwise

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_space_separated_numbers(string):
  return [int(number) for number in re.findall(r'(-?\d+)', string)]

def parse_file(file):
  with open(file) as input:
    return [parse_space_separated_numbers(line) for line in input.readlines()]

def next_number(sequence):
  if all(n == 0 for n in sequence):
    return 0
  return sequence[-1] + next_number([b - a for a,b in pairwise(sequence)])

def prev_number(sequence):
  if all(n == 0 for n in sequence):
    return 0
  return sequence[0] - prev_number([b - a for a,b in pairwise(sequence)])

def part_1(file):
  sequences = parse_file(file)
  next_numbers = [next_number(sequence) for sequence in sequences]
  return sum(next_numbers)

def part_2(file):
  sequences = parse_file(file)
  prev_numbers = [prev_number(sequence) for sequence in sequences]
  return sum(prev_numbers)

# Solution
print(part_1(INPUT_FILE)) # 1789635132
print(part_2(INPUT_FILE)) # 913

# Tests
assert part_1(TEST_FILE) == 114
assert part_2(TEST_FILE) == 2
