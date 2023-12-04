#! /usr/bin/env python3
import os
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

# We keep line ends so that numbers at the end of a line
# and start of the next one don't get read as one number
def file_gen(file):
  with open(file) as input:
    for i, line in enumerate(input.readlines()):
      for j, char in enumerate(line):
        yield i, j, char

# We keep line ends so that numbers at the end of a line
# and start of the next one don't get read as one number
def string_gen(string):
  for i, line in enumerate(string.splitlines(keepends=True)):
      for j, char in enumerate(line):
        yield i, j, char

def eight_adjacents(point):
  i, j = point
  return {
    (i-1, j-1), (i-1, j), (i-1, j+1),
    (i  , j-1),           (i  , j+1),
    (i+1, j-1), (i+1, j), (i+1, j+1),
  }

class SchemaNumber:
  def __init__(self) -> None:
    self.digits = []
    self.coords = set()

  def append(self, coord, digit):
    self.digits.append(digit)
    self.coords.add(coord)

  def value(self):
    return 0 if len(self.digits) == 0 else int(''.join(self.digits))
  
  def adjacents(self):
    return reduce(lambda adjacents, coord: adjacents | eight_adjacents(coord), self.coords, set()) - self.coords


def parse_input(input, file=True):
  symbols = {}
  numbers = []
  digits = {}

  current_number = SchemaNumber()

  # accept both file and string input to make testing easier
  iterator = file_gen(input) if file else string_gen(input)

  for i, j, char in iterator:
    if char in '0123456789':
      current_number.append((i, j), char)
      digits[(i, j)] = current_number
    else:
      if current_number.value() != 0: # end of number
        numbers.append(current_number)
        current_number = SchemaNumber()
      if char not in '.\n':
        symbols[(i, j)] = char

  return symbols, numbers, digits

# A gear is any * symbol that is adjacent to exactly two part numbers.
# Its gear ratio is the result of multiplying those two numbers together.
def gear_ratio(digits, gear):
  gear_coord, _ = gear
  gear_adjacent_coords = eight_adjacents(gear_coord)
  adjacent_numbers = {digits[coord] for coord in gear_adjacent_coords if coord in digits}
  if len(adjacent_numbers) == 2:
    return adjacent_numbers.pop().value() * adjacent_numbers.pop().value()
  return 0

# find all numbers that are part numbers
def part_1(input, file=True):
  symbols, numbers, _ = parse_input(input, file)
  part_numbers = filter(lambda number: number.adjacents() & symbols.keys(), numbers)
  return sum(number.value() for number in part_numbers)

# find the gear ratio of every gear and add them all up
def part_2(input, file=True):
  symbols, _, digits = parse_input(input, file)
  # I'll consider all * gears, but only the correct gears will have a non zero gear ratio
  gears = filter(lambda symbol: symbol[1] == '*', symbols.items())
  return sum(gear_ratio(digits, gear) for gear in gears)

# Solution
print(part_1(INPUT_FILE)) # 519444
print(part_2(INPUT_FILE)) # 74528807

# Tests
assert part_1(TEST_FILE) == 4361
assert part_2(TEST_FILE) == 467835

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
