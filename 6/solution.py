#! /usr/bin/env python3
import os
import re
from math import sqrt, ceil, floor
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_space_separated_numbers(string):
  return [int(number) for number in re.findall(r'(\d+)', string)]

def read_as_one_number(string):
  numbers = re.search(r'[0-9 ]+', string)
  number = re.sub(' ', '', numbers.group(0))
  return int(number)

def product(numbers):
  return reduce(lambda x,y: x*y, numbers)

def parse_file_part_1(file):
  with open(file) as input:
    times, distances = [parse_space_separated_numbers(line) for line in input.readlines()]
    races = list(zip(times, distances))
    return races
  
def parse_file_part_2(file):
  with open(file) as input:
    time, distance = [read_as_one_number(line) for line in input.readlines()]
    return time, distance
  
# b is how long the button is pressed
# t is the total time for the race
# d is the distance the car will travel
# d = b*(t - b)  or  -b**2 + tb - d = 0
def ways_to_win(race):
  time, distance_to_beat = race
  root1 = (- time + sqrt(time**2 - 4*distance_to_beat) )/(-2)
  root2 = (- time - sqrt(time**2 - 4*distance_to_beat) )/(-2)
  if int(root1) == root1:
    return root2 - root1 - 1
  return floor(root2) - floor(root1)

def part_1(file):
  races = parse_file_part_1(file)
  nb_of_ways_to_win = [ways_to_win(race) for race in races]
  return product(nb_of_ways_to_win)

def part_2(file):
  race = parse_file_part_2(file)
  return ways_to_win(race)

# Solution
print(part_1(INPUT_FILE)) # 219849
print(part_2(INPUT_FILE)) # 29432455

# Tests
assert part_1(TEST_FILE) == 288
assert part_2(TEST_FILE) == 71503
