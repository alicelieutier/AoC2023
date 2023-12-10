#! /usr/bin/env python3
import os
from functools import reduce

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def file_gen(file):
  with open(file) as input:
    return (line.strip() for line in input.readlines())

def string_gen(string):
  return (line for line in string.splitlines() if line != '')

def step(pos, dir):
  i, j = pos
  return {
    'N': (i-1, j),
    'W': (i,j-1),
    'E': (i,j+1),
    'S': (i+1,j),
  }[dir]

def next_direction(sketch, pos, last_direction):
  x, y = pos
  match char := sketch[x][y]:
    case '|' | '-': return last_direction # continue in the same direction
    case 'F': return 'E' if last_direction == 'N' else 'S'
    case '7': return 'W' if last_direction == 'N' else 'S'
    case 'J': return 'W' if last_direction == 'S' else 'N'
    case 'L': return 'E' if last_direction == 'S' else 'N'
    case _: raise Exception(f'Not a pipe character: {char} at {x, y}')

def find_start(sketch):
  for i, line in enumerate(sketch):
    if (pos := line.find('S')) != -1:
      return (i, pos)
    
def starting_directions(sketch, start):
  def aux(direction):
    x, y = step(start, direction)
    return sketch[x][y] in {
      'N': '|7F',
      'E': '-J7',
      'W': '-FL',
      'S': '|LJ',
    }[direction]
  return filter(aux, 'NEWS')

def walk_loop(sketch, start, direction):
  x, y = step(start, direction)
  loop = [(start, direction)]
  while sketch[x][y] != 'S':
    loop.append(((x,y), direction))
    direction = next_direction(sketch, (x,y), direction)
    x, y = step((x,y), direction)
  return loop

def left_right(sketch, pos, direction):
  x,y = pos
  char = sketch[x][y]
  match char, direction:
    case '|', 'N': return {step(pos, 'W')}, {step(pos, 'E')}
    case '|', 'S': return {step(pos, 'E')}, {step(pos, 'W')}
    case '-', 'E': return {step(pos, 'N')}, {step(pos, 'S')}
    case '-', 'W': return {step(pos, 'S')}, {step(pos, 'N')}
    case 'F', 'N': return {step(pos, 'W'), step(pos, 'N')}, set()
    case 'F', 'W': return set(), {step(pos, 'W'), step(pos, 'N')}
    case '7', 'N': return set(), {step(pos, 'E'), step(pos, 'N')}
    case '7', 'E': return {step(pos, 'E'), step(pos, 'N')}, set()
    case 'J', 'S': return {step(pos, 'E'), step(pos, 'S')}, set()
    case 'J', 'E': return set(), {step(pos, 'E'), step(pos, 'S')}
    case 'L', 'S': return set(), {step(pos, 'W'), step(pos, 'S')} 
    case 'L', 'W': return {step(pos, 'W'), step(pos, 'S')}, set()
    case 'S', _: return set(), set() # not ideal, but we're not marking the start
    case _: raise Exception(f'Not a pipe character: {char} at {(x, y)}')

def mark_loop(sketch, loop):
  height, width = len(sketch), len(sketch[0])
  loop_tiles = set([pos for pos, _ in loop])
  def aux(acc, element):
    pos, direction = element
    left_tiles, right_tiles = acc
    left, right = left_right(sketch, pos, direction)
    left = set(filter(lambda pos: within_limits(width, height, pos), left)) - loop_tiles
    right = set(filter(lambda pos: within_limits(width, height, pos), right)) - loop_tiles
    return left_tiles | left, right_tiles | right
  return reduce(aux, loop, (set(), set()))

def within_limits(width, height, pos):
  i, j = pos
  return i >= 0 and i < height and j >= 0 and j < width

def adjacents_within_limits(width, height, pos):
  i, j = pos
  adjacents = [
    (i-1, j-1), (i-1, j), (i-1, j+1),
    (i  , j-1),           (i  , j+1),
    (i+1, j-1), (i+1, j), (i+1, j+1),
  ]
  return set(filter(lambda pos: within_limits(width, height, pos) ,adjacents))

def viz(sketch, hashes, ohs, dots):
  new_sketch = []
  for i, line in enumerate(sketch):
    new_sketch.append([])
    for j, char in enumerate(line):
      if (i, j) in hashes:
        new_sketch[i].append('#')
      elif (i, j) in ohs:
        new_sketch[i].append('O')
      elif (i, j) in dots:
        new_sketch[i].append('.')
      else:
        new_sketch[i].append(char)
  print('\n'.join([''.join(line) for line in new_sketch]))

def fill_space(width, height, walls, starting_tiles):
  tiles = set(starting_tiles)
  to_visit = set(starting_tiles)
  while len(to_visit) > 0:
    pos = to_visit.pop()
    tiles.add(pos)
    adjacents = adjacents_within_limits(width, height, pos)
    to_visit |= (adjacents - (walls | tiles))
  return tiles

def parse_input(input, is_file=True):
  return list(file_gen(input) if is_file else string_gen(input))

def part_1(input, is_file=True):
  sketch = parse_input(input, is_file)
  start = find_start(sketch)
  starting_dir = list(starting_directions(sketch, start))[0]
  loop = walk_loop(sketch, start, starting_dir)
  return len(loop) // 2

def part_2(input, is_file=True):
  sketch = parse_input(input, is_file)
  start = find_start(sketch)
  starting_dir = list(starting_directions(sketch, start))[0]

  loop = walk_loop(sketch, start, starting_dir)
  height, width = len(sketch), len(sketch[0])

  left_tiles, right_tiles = mark_loop(sketch, loop)
  loop_tiles = set([pos for pos, _ in loop])

  left_tiles = fill_space(width, height, loop_tiles, left_tiles)
  right_tiles = fill_space(width, height, loop_tiles, right_tiles)

  viz(sketch, left_tiles, right_tiles, loop_tiles)

  if (0,0) in left_tiles:
    return len(right_tiles)
  return len(left_tiles)

# Solution
print(part_1(INPUT_FILE))
print(part_2(INPUT_FILE))

# Tests
TESTCASES_PART_1 = [
('''
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
''', 4),
('''
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
''', 8),
]

for string, result in TESTCASES_PART_1:
  assert part_1(string, is_file=False) == result

TESTCASES_PART_2 = [
('''
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
''', 4),
('''
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
''', 4),
('''
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
''', 8),
('''
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
''', 10),
]

for string, result in TESTCASES_PART_2:
  assert part_2(string, is_file=False) == result