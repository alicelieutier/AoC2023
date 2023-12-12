#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
import re
from itertools import combinations

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  springs, numbers = line.split(' ')
  return springs, [int(nb) for nb in numbers.split(',')]

def parse_file_part_1(file):  
  with open(file) as input:
    return [parse_line(line.strip()) for line in input.readlines()]
  
def is_valid(row):
  springs, numbers = row
  spring_patches = re.findall(r'(#+)', springs)
  return [len(patch) for patch in spring_patches] == numbers

def potential_springs_positions(springs):
  return [i for i, char in enumerate(springs) if char =='?']

def arrangements(row):
  springs, numbers = row
  real_springs = springs.count('#')
  potential_springs = springs.count('?')
  total = sum(numbers)
  print(f'We need to place {total - real_springs} springs on {potential_springs} spots')
  
  counter = 0

  for indices in combinations(potential_springs_positions(springs), total - real_springs):
    trial_springs = list(springs)
    for index in indices:
      trial_springs[index] = '#'
    # print('Trying', ''.join(trial_springs), numbers)
    if is_valid((''.join(trial_springs),numbers)):
      counter += 1

  return counter

def part_1(file):
  rows = parse_file_part_1(file)
  return sum(arrangements(row) for row in rows)

# Solution
print(part_1(INPUT_FILE))

# Tests
assert is_valid(('.###.##.#...', [3,2,1])) == True
assert is_valid(('.###.##.#...', [3,1,1])) == False
assert is_valid(('####.##.#...', [2,2,2,1])) == False
assert is_valid(('####', [4])) == True


assert arrangements(('???.###',[1,1,3])) == 1
assert arrangements(('.??..??...?##.',[1,1,3])) == 4
assert arrangements(('?###????????',[3,2,1])) == 10

assert(part_1(TEST_FILE)) == 21
