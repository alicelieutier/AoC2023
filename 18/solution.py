#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from functools import reduce
from itertools import count
from math import inf

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def better_range(a,b):
  if a < b: return range(a,b)
  return range(a,b,-1)

def get_boundaries(points, margin=0):
  def aux(acc, point):
    x,y = point
    min_x, max_x, min_y, max_y = acc
    return min(min_x,x), max(max_x,x), min(min_y,y), max(max_y,y)
  min_x, max_x, min_y, max_y = reduce(aux, points, (inf,-inf,inf,-inf))
  return min_x-margin, max_x+margin, min_y-margin, max_y+margin

def viz(hashes, ohs=set()):
  min_x, max_x, min_y, max_y = get_boundaries(hashes, 0)
  new_sketch = []
  for i, new_i in zip(range(min_x, max_x+1), count()):
    new_sketch.append([])
    for j in range(min_y, max_y+1):
      if (i, j) in hashes:
        new_sketch[new_i].append('#')
      elif (i, j) in ohs:
        new_sketch[new_i].append('O')
      else:
        new_sketch[new_i].append('.')
  print('\n'.join([''.join(line) for line in new_sketch]))

def parse_line(line):
  direction, number, color = line.split(' ')
  return direction, int(number), color.strip('()')

def parse_file(file):  
  with open(file) as input:
    return [parse_line(line.strip()) for line in input.readlines()]

def adjacents(pos):
  i, j = pos
  return {
    (i-1, j-1), (i-1, j), (i-1, j+1),
    (i  , j-1),           (i  , j+1),
    (i+1, j-1), (i+1, j), (i+1, j+1),
  }

def fill_space(walls, start=(1,1)):
  tiles = set()
  to_visit = {start}
  while to_visit:
    pos = to_visit.pop()
    tiles.add(pos)
    to_visit |= (adjacents(pos) - (walls | tiles))
  return tiles

def edges(dig_plan):
  edges = set()
  pos = (0,0)
  for direction, number, _ in dig_plan:
    for _ in range(number):
      match direction:
        case 'R':
          pos = pos[0],pos[1]+1
          edges.add(pos)
        case 'L':
          pos = pos[0],pos[1]-1
          edges.add(pos)
        case 'U':
          pos = pos[0]-1,pos[1]
          edges.add(pos)
        case 'D':
          pos = pos[0]+1,pos[1]
          edges.add(pos)
  return edges

def part_1(file):
  dig_plan = parse_file(file)
  edges_points = edges(dig_plan)
  tiles = fill_space(edges_points)
  # viz(edges_points, tiles)
  return len(edges_points | tiles)

# Solution
print(part_1(INPUT_FILE))

# Tests
assert(part_1(TEST_FILE)) == 62
