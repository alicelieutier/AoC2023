#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
# from itertools import count
# from functools import cache
from enum import Enum
from collections import deque

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class Dir(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

def opposite(direction: Dir):
  match direction:
    case Dir.UP: return Dir.DOWN
    case Dir.DOWN: return Dir.UP
    case Dir.RIGHT: return Dir.LEFT
    case Dir.LEFT: return Dir.RIGHT
   
def parse_file(file):  
  with open(file) as input:
    return [[int(char) for char in line.strip()] for line in input.readlines()]

# def viz(image):
#   print('\n'.join([f'{i} {''.join(line)}' for i, line in enumerate(image)]))
#   print('')

def within_limits(city_map, pos):
  height, width = len(city_map), len(city_map[0])
  i, j = pos
  return i >= 0 and i < height and j >= 0 and j < width

def next_cell(pos, direction: Dir):
  i, j = pos
  adjacents = {
    Dir.UP: (i-1,j),
    Dir.DOWN: (i+1,j),
    Dir.RIGHT: (i,j+1),
    Dir.LEFT: (i,j-1),
  }
  adjacents.pop(opposite(direction))
  return adjacents.items()

def viz(city_map, hashes=set()):
  height, width = len(city_map), len(city_map[0])
  for i in range(height):
    line = []
    for j in range(width):
      if (i,j) in hashes:
        line.append('#')
      else:
        line.append(str(city_map[i][j]))
    print(''.join(line))

def manhattan(a,b):
  xa, ya = a
  xb, yb = b
  return abs(xb - xa) + abs(yb - ya)

def heatloss_at_pos(city_map, pos):
  i,j = pos
  return city_map[i][j]

MAX = 100000000000000
def best_path(city_map, start, end):
  visited = set()
  start_node = (start, Dir.RIGHT, -1)
  to_visit = {start_node}
  heatloss = {start_node: 0}
  path_to = {start_node: []}

  def min_key(node):
    pos, _, _ = node
    return heatloss[node] + manhattan(pos, end)

  while to_visit:
    # find minimum node using heuristic
    node = min(to_visit, key=min_key)
    to_visit.remove(node)
    pos, direction, steps_in_dir = node

    if pos == end:
      return heatloss[node], path_to[node]

    visited.add(node)

    for next_dir, next_pos in next_cell(pos, direction):
      if not within_limits(city_map, next_pos):
        continue
      if steps_in_dir > 1 and next_dir == direction:
        continue
      next_steps_in_dir = 0 if next_dir != direction else steps_in_dir + 1
      next_node = (next_pos, next_dir, next_steps_in_dir)

      if next_node in visited:
        continue

      heatloss[next_node] = min(heatloss.get(next_node, MAX), heatloss[node] + heatloss_at_pos(city_map, next_pos))
      path_to[next_node] = path_to[node] + [pos]

      to_visit.add(next_node)

def part_1(file):
  city_map = parse_file(file)
  height, width = len(city_map), len(city_map[0])
  heatloss, path = best_path(city_map, (0,0), (height-1, width-1))
  viz(city_map, set(path))
  print(heatloss)
  return heatloss

# Solution
print(part_1(INPUT_FILE)) # 797

# Tests
assert(part_1(TEST_FILE)) == 102
