#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from itertools import pairwise

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line_part_1(line):
  direction, number, _ = line.split(' ')
  return direction, int(number)

def parse_file_part_1(file):  
  with open(file) as input:
    return [parse_line_part_1(line.strip()) for line in input.readlines()]
  
def parse_line_part_2(line):
  color = line.split(' ')[-1]
  direction = 'RDLU'[int(color[-2])]
  number = int(color[2:-2], 16)
  return direction, number

def parse_file_part_2(file):  
  with open(file) as input:
    return [parse_line_part_2(line.strip()) for line in input.readlines()]
  
def area(dig_plan):
  space = 0
  i = 0
  for direction, number in dig_plan:
    match direction:
      case 'R': space -= i*number
      case 'L': space += i*number
      case 'U': i -= number
      case 'D': i += number
  return space

def perimeter(dig_plan):
  return sum(distance for _, distance in dig_plan)

def total_area(dig_plan):
  a = area(dig_plan)
  p = perimeter(dig_plan)
  # pick theorem formula
  return int(a + (p/2) + 1)

def part_1(file):
  dig_plan = parse_file_part_1(file)
  return total_area(dig_plan)

def part_2(file):
  dig_plan = parse_file_part_2(file)
  return total_area(dig_plan)

# Solution
print(part_1(INPUT_FILE)) # 36807
print(part_2(INPUT_FILE)) # 48797603984357

# Tests
assert part_1(TEST_FILE) == 62
assert part_2(TEST_FILE) == 952408144115
