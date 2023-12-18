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

# Finding the x,y coordinates of the polygon envelope
def vertices(dig_plan):
  i,j = 0,0
  yield 0,0
  for (direction, number),(next_dir,_) in pairwise(dig_plan):
    match direction, next_dir:
      case 'R', 'D':
        i,j = i, j+number
        yield i, j+1
      case 'R', 'U':
        i,j = i, j+number
        yield i, j
      case 'L', 'D':
        i,j = i, j-number
        yield i+1, j+1
      case 'L', 'U':
        i,j = i, j-number
        yield i+1, j
      case 'D', 'R':
        i,j = i+number, j
        yield i, j+1
      case 'D', 'L':
        i,j = i+number, j
        yield i+1, j+1
      case 'U', 'R':
        i,j = i-number, j
        yield i, j
      case 'U', 'L':
        i,j = i-number, j
        yield i+1, j

def alternate():
  while True:
    yield 1
    yield -1

def total_space(vertices):
  return sum(polarity*x*y for polarity, (x,y) in zip(alternate(), vertices))

def part_1(file):
  dig_plan = parse_file_part_1(file)
  return total_space(vertices(dig_plan))

def part_2(file):
  dig_plan = parse_file_part_2(file)
  return total_space(vertices(dig_plan))

# Solution
print(part_1(INPUT_FILE)) # 36807
print(part_2(INPUT_FILE)) # 48797603984357

# Tests
assert part_1(TEST_FILE) == 62
assert part_2(TEST_FILE) == 952408144115
