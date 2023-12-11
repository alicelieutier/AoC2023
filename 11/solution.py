#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from itertools import combinations

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_file(file):  
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def viz(image):
  print('\n'.join([''.join(line) for line in image]))

def expand_vertically(image):
  vertical_expansion = []
  for line in image:
    vertical_expansion.append(line)
    if '#' not in line:
      vertical_expansion.append(line)
  return vertical_expansion

def rotated(image):
  height, width = len(image), len(image[0])
  new_image = [['.' for _ in range(height)] for _ in range(width)]
  for i, line in enumerate(image):
    for j, char in enumerate(line):
      new_image[j][i] = char
  return new_image
  
def expand(image):
  new_image = expand_vertically(rotated(image))
  return expand_vertically(rotated(new_image))

def expand2(image):
  empty_lines = [i for i, line in enumerate(image) if '#' not in line]
  empty_rows = [j for j, line in enumerate(rotated(image)) if '#' not in line]
  new_image = []
  for i, line in enumerate(image):
    new_image.append([])
    for j, char in enumerate(line):
      if i in empty_lines or j in empty_rows:
        new_image[i].append('$')
      else:
        new_image[i].append(char)
  return new_image

def find_galaxies(image):
  return [(i,j) for i, line in enumerate(image)
          for j, char in enumerate(line) if image[i][j] == '#']

def manhattan(a,b):
  xa, ya = a
  xb, yb = b
  return abs(xb - xa) + abs(yb - ya)

def better_range(a,b):
  if a < b: return range(a,b)
  return range(b,a)

def manhattan2(image, a,b, e=1000000):
  xa, ya = a
  xb, yb = b
  distance = 0
  for i in better_range(xa, xb):
    if image[i][ya] == '$':
      distance += e
    else:
      distance += 1
  for j in better_range(ya, yb):
    if image[xb][j] == '$':
      distance += e
    else:
      distance += 1
  return distance

def part_1(file):
  image = parse_file(file)
  expanded_image = expand(image)
  galaxies = find_galaxies(expanded_image)
  return sum(manhattan(a,b) for a,b in combinations(galaxies, 2))

def part_2(file, e=1000000):
  image = parse_file(file)
  expanded_image = expand2(image)
  galaxies = find_galaxies(expanded_image)
  return sum(manhattan2(expanded_image, a, b, e) for a,b in combinations(galaxies, 2))

# Solution
print(part_1(INPUT_FILE)) # 9799681
print(part_2(INPUT_FILE))


# Tests
assert(part_1(TEST_FILE)) == 374
assert(part_2(TEST_FILE, e=10)) == 1030
assert(part_2(TEST_FILE, e=100)) == 8410
