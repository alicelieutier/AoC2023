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

def rotated(image):
  height, width = len(image), len(image[0])
  new_image = [['.' for _ in range(height)] for _ in range(width)]
  for i, line in enumerate(image):
    for j, char in enumerate(line):
      new_image[j][i] = char
  return new_image

def expand(image):
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

def better_range(a,b):
  if a < b: return range(a,b)
  return range(a,b,-1)

def distance(image, a, b, e=2):
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

def process(file, e=2):
  image = parse_file(file)
  expanded_image = expand(image)
  galaxies = find_galaxies(expanded_image)
  return sum(distance(expanded_image, a, b, e) for a,b in combinations(galaxies, 2))

# Solution
print(process(INPUT_FILE)) # 9799681
print(process(INPUT_FILE, e=1000000)) # 513171773355

# Tests
assert(process(TEST_FILE)) == 374
assert(process(TEST_FILE, e=10)) == 1030
assert(process(TEST_FILE, e=100)) == 8410
