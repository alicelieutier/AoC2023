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

def find_galaxies(image):
  return [(i,j) for i, line in enumerate(image)
          for j, char in enumerate(line) if image[i][j] == '#']

def manhattan(a,b):
  xa, ya = a
  xb, yb = b
  return abs(xb - xa) + abs(yb - ya)

def part_1(file):
  image = parse_file(file)
  expanded_image = expand(image)
  galaxies = find_galaxies(expanded_image)
  return sum(manhattan(a,b) for a,b in combinations(galaxies, 2))

# Solution
print(part_1(INPUT_FILE))

# Tests
assert(part_1(TEST_FILE)) == 374
