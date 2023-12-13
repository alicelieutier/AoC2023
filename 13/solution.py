#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
from itertools import pairwise

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_block(block):
  return block.splitlines()

def parse_file(file):  
  with open(file) as input:
    return [parse_block(block) for block in input.read().split('\n\n')]
  
def rotated(block):
  height, width = len(block), len(block[0])
  new_block = [['.' for _ in range(height)] for _ in range(width)]
  for i, line in enumerate(block):
    for j, char in enumerate(line):
      new_block[j][i] = char
  return [''.join(reversed(line)) for line in new_block]

def viz(image):
  print('\n'.join([f'{i} {''.join(line)}' for i, line in enumerate(image)]))

def check_reflection(pattern, index):
  for i, j in zip(range(index, -1, -1),range(index+1, len(pattern))):
    if pattern[i] != pattern[j]:
      return False
  return True

def horizontal_reflection(pattern):
  for i, (line1, line2) in enumerate(pairwise(pattern)):
    if line1 == line2:
      if check_reflection(pattern, i):
        return i+1
  return 0

def hamming_distance(string1, string2):
  return sum(c1 != c2 for c1, c2 in zip(string1, string2))

def check_reflection_with_smudge(pattern, index):
  smudge_found = False
  for i, j in zip(range(index, -1, -1),range(index+1, len(pattern))):
    if pattern[i] != pattern[j]:
      if hamming_distance(pattern[i], pattern[j]) == 1 and not smudge_found:
        smudge_found = True
        continue
      return False
  return True if smudge_found else False

def horizontal_reflection_with_smudge(pattern):
  for i, (line1, line2) in enumerate(pairwise(pattern)):
    if hamming_distance(line1, line2) < 2:
      if check_reflection_with_smudge(pattern, i):
        return i+1
  return 0

def summarize(pattern):
  h = horizontal_reflection(pattern)
  if h > 0: return 100*h

  new_pattern = rotated(pattern)
  v = horizontal_reflection(new_pattern)
  if v > 0: return v

  raise Exception('No reflection found in pattern!')

def summarize_with_smudge(pattern):
  h = horizontal_reflection_with_smudge(pattern)
  if h > 0: return 100*h

  new_pattern = rotated(pattern)
  v = horizontal_reflection_with_smudge(new_pattern)
  if v > 0: return v

  raise Exception('No reflection found in pattern!')

def part_1(file):
  patterns = parse_file(file)
  return sum(summarize(pattern) for pattern in patterns)

def part_2(file):
  patterns = parse_file(file)
  return sum(summarize_with_smudge(pattern) for pattern in patterns)

# Solution
print(part_1(INPUT_FILE))
print(part_2(INPUT_FILE))

# Tests
assert(part_1(TEST_FILE)) == 405
assert(part_2(TEST_FILE)) == 400

assert horizontal_reflection(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#']) == 4