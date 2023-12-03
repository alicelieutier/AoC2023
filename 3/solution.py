#! /usr/bin/env python3
import os
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

# We keep line ends so that numbers at the end of a line
# an start of the next one don't get read as one number
def file_gen(file):
  with open(file) as input:
    for i, line in enumerate(input.readlines()):
      for j, char in enumerate(line):
        yield i, j, char

# We keep line ends so that numbers at the end of a line
# an start of the next one don't get read as one number
def string_gen(string):
  for i, line in enumerate(string.splitlines(keepends=True)):
      for j, char in enumerate(line):
        yield i, j, char

def parse_input(input, file=True):
  symbols = {}
  numbers = []

  current_number = 0
  current_number_coords = set()

  iterator = file_gen(input) if file else string_gen(input)

  for i, j, char in iterator:
    if char in '0123456789':
      current_number = current_number * 10 + int(char)
      current_number_coords.add((i,j))
    else:
      if current_number != 0: # end of number
        numbers.append((current_number, current_number_coords))
        current_number = 0
        current_number_coords = set()
      if char not in '.\n':
        symbols[(i, j)] = char
  return symbols, numbers


def eight_neighbours(point):
  i, j = point
  return {
    (i-1, j-1), (i-1, j), (i-1, j+1),
    (i, j-1),             (i, j+1),
    (i+1, j-1), (i+1, j), (i+1, j+1),
  }

def has_symbol_neighbour(symbols):
  def aux(number_item):
    _, coords = number_item
    number_neighbours = reduce(lambda neighbours, coord: neighbours | eight_neighbours(coord), coords, set()) - coords
    return len(number_neighbours & symbols.keys()) > 0
  return aux


def part_1(input, file=True):
  symbols, numbers = parse_input(input, file)
  part_numbers = filter(has_symbol_neighbour(symbols), numbers)
  return sum(number for number, _ in part_numbers)


# Solution
print(part_1(INPUT_FILE)) # 519444

# Tests

assert part_1(TEST_FILE) == 4361

TESTCASES = [
('''
.......
.1304..
...*...
''', 1304),
('''
.....46
4+.....
''', 4),
('''
.....46
46..-..
''', 46),
]

for string, result in TESTCASES:
  assert part_1(string, file=False) == result


