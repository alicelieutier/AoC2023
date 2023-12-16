#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from enum import Enum

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class Dir(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

def parse_file(file):  
  with open(file) as input:
    devices = {}
    height, width = 0,0
    for i, line in enumerate(input.readlines()):
      height = i+1
      for j, char in enumerate(line.strip()):
        width = j+1
        if char != '.':
          devices[(i,j)] = char
    return devices, (height, width)
  
def viz(dimensions, hashes):
  height, width = dimensions
  for i in range(height):
    line = []
    for j in range(width):
      if (i,j) in hashes:
        line.append('#')
      else:
        line.append('.')
    print(''.join(line))

def within_limits(pos, dimensions):
  height, width = dimensions
  i, j = pos
  return i >= 0 and i < height and j >= 0 and j < width

def next_pos(pos, direction: Dir):
  i, j = pos
  match direction:
    case Dir.UP: return (i-1,j), direction
    case Dir.DOWN: return (i+1,j), direction
    case Dir.RIGHT: return (i,j+1), direction
    case Dir.LEFT: return (i,j-1), direction

def next_pos_with_device(device, pos, direction: Dir) -> list:
  match device, direction:
    case ('|', Dir.RIGHT | Dir.LEFT):
      return [next_pos(pos, Dir.UP), next_pos(pos, Dir.DOWN)]
    case ('-', Dir.UP | Dir.DOWN):
      return [next_pos(pos, Dir.RIGHT), next_pos(pos, Dir.LEFT)]
    case ('/', Dir.UP):
      return [next_pos(pos, Dir.RIGHT)]
    case ('/', Dir.DOWN):
      return [next_pos(pos, Dir.LEFT)]
    case ('/', Dir.RIGHT):
      return [next_pos(pos, Dir.UP)]
    case ('/', Dir.LEFT):
      return [next_pos(pos, Dir.DOWN)]
    case ('\\', Dir.UP):
      return [next_pos(pos, Dir.LEFT)]
    case ('\\', Dir.DOWN):
      return [next_pos(pos, Dir.RIGHT)]
    case ('\\', Dir.RIGHT):
      return [next_pos(pos, Dir.DOWN)]
    case ('\\', Dir.LEFT):
      return [next_pos(pos, Dir.UP)]
    case _:
      return [next_pos(pos, direction)]

def light_ray(devices, dimensions, start):
  light = set()
  energised_cells = set()
  todo = {start}

  while len(todo) > 0:
    pos, direction = todo.pop()
    if not within_limits(pos, dimensions):
      continue
    if (pos, direction) in light:
      continue

    light.add((pos, direction))
    energised_cells.add(pos)

    todo |= set(next_pos_with_device(devices.get(pos), pos, direction))

  return energised_cells

def possible_starts(dimensions):
  height, width = dimensions
  for i in range(height):
    yield ((i, 0), Dir.RIGHT)
    yield ((i, width-1), Dir.LEFT)
  for j in range(height):
    yield ((0, j), Dir.DOWN)
    yield ((height-1, j), Dir.UP)

def part_1(file):
  devices, dimensions = parse_file(file)
  return len(light_ray(devices, dimensions, ((0,0), Dir.RIGHT)))

def part_2(file):
  devices, dimensions = parse_file(file)
  return max(len(light_ray(devices, dimensions, start)) for start in possible_starts(dimensions))

# Solution
print(part_1(INPUT_FILE)) # 7728
print(part_2(INPUT_FILE)) # 8061

# Tests
assert(part_1(TEST_FILE)) == 46
assert(part_2(TEST_FILE)) == 51
