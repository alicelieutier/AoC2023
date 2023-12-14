#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from itertools import count
from functools import cache

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_file(file):  
  with open(file) as input:
    return tuple(line.strip() for line in input.readlines())

def viz(image):
  print('\n'.join([f'{i} {''.join(line)}' for i, line in enumerate(image)]))
  print('')

@cache
def tilt_north(platform):
  platform = [list(line) for line in platform]
  width, height = len(platform[0]), len(platform)
  for j in range(width):
    last_open_pos = 0
    for i in range(height):
      char = platform[i][j]
      if char == '#':
        last_open_pos = i+1
      if char == 'O':
        platform[i][j] = platform[last_open_pos][j]
        platform[last_open_pos][j] = char
        last_open_pos += 1
  return tuple(''.join(line) for line in platform)

@cache
def tilt_south(platform):
  platform = [list(line) for line in platform]
  width, height = len(platform[0]), len(platform)
  for j in range(width):
    last_open_pos = height-1
    for i in range(height-1, -1, -1):
      char = platform[i][j]
      if char == '#':
        last_open_pos = i-1
      if char == 'O':
        platform[i][j] = platform[last_open_pos][j]
        platform[last_open_pos][j] = char
        last_open_pos -= 1
  return tuple(''.join(line) for line in platform)

@cache
def tilt_west(platform):
  platform = [list(line) for line in platform]
  width, height = len(platform[0]), len(platform)
  for i in range(height):
    last_open_pos = 0
    for j in range(width):
      char = platform[i][j]
      if char == '#':
        last_open_pos = j+1
      if char == 'O':
        platform[i][j] = platform[i][last_open_pos]
        platform[i][last_open_pos] = char
        last_open_pos += 1
  return tuple(''.join(line) for line in platform)

@cache
def tilt_east(platform):
  platform = [list(line) for line in platform]
  width, height = len(platform[0]), len(platform)
  for i in range(height):
    last_open_pos = width-1
    for j in range(width-1, -1, -1):
      char = platform[i][j]
      if char == '#':
        last_open_pos = j-1
      if char == 'O':
        platform[i][j] = platform[i][last_open_pos]
        platform[i][last_open_pos] = char
        last_open_pos -= 1
  return tuple(''.join(line) for line in platform)

@cache
def cycle(platform):
  platform = tilt_north(platform)
  platform = tilt_west(platform)
  platform = tilt_south(platform)
  platform = tilt_east(platform)
  return platform

def load(platform):
  height = len(platform)
  return sum(row.count('O')*weight for row, weight in zip(platform, count(height,-1)))


def part_1(file):
  platform = parse_file(file)
  tilted_platform = tilt_north(platform)
  return load(tilted_platform)

def part_2(file, cycles=1000000000):
  platform = parse_file(file)

  offset = 0
  cycle_length = 0
  last_seen = {platform: 0}

  for i in count(1):
    platform = cycle(platform)

    if platform in last_seen:
      offset = last_seen[platform]
      cycle_length = i - last_seen[platform]
      break

    last_seen[platform] = i

  final_platform_number = offset + (1000000000 - offset) % cycle_length
  final_platform = [key for key, value in last_seen.items() if value == final_platform_number][0]

  return load(final_platform)

# Solution
print(part_1(INPUT_FILE)) # 109098
print(part_2(INPUT_FILE)) # 100064

# Tests
assert tilt_north(('##..','O.O.','..#O','OOO.')) == ('##OO','OO..','O.#.','..O.')

assert(part_1(TEST_FILE)) == 136
assert(part_2(TEST_FILE)) == 64
assert(part_1(INPUT_FILE)) == 109098
assert(part_2(INPUT_FILE)) == 100064