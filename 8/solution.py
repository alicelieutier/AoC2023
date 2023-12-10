#! /usr/bin/env python3
import os
import re
from itertools import cycle
from functools import reduce
from math import lcm

TEST_FILE_1 = f'{os.path.dirname(__file__)}/test_input_1'
TEST_FILE_2 = f'{os.path.dirname(__file__)}/test_input_2'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  node, left, right = re.findall(r'([12A-Z]{3})', line)
  return node, (left, right)

def parse_file(file):
  with open(file) as input:
    lines = input.readlines()
    instructions = lines[0].strip()
    nodes = dict(parse_line(line.strip()) for line in lines[2:])
    return instructions, nodes

def length_to_end(nodes, instructions, starting_node, end_condition):
  directions = cycle(instructions)
  current_node = starting_node
  nb_steps = 0
  while not end_condition(current_node):
    step = next(directions)
    if step == 'R':
      current_node = nodes[current_node][1]
    else:
      current_node = nodes[current_node][0]
    nb_steps += 1
  return nb_steps
    
def part_1(file):
  instructions, nodes = parse_file(file)
  return length_to_end(
    nodes, instructions,
    'AAA', lambda node: node == 'ZZZ')

def part_2(file):
  instructions, nodes = parse_file(file)
  starting_nodes = [node for node in nodes.keys() if node[-1] == 'A']
  lengths = [length_to_end(
    nodes, instructions,
    starting_node, lambda node: node[-1] == 'Z')
    for starting_node in starting_nodes]
  return lcm(*lengths)

# Solution
print(part_1(INPUT_FILE)) # 24253
print(part_2(INPUT_FILE)) # 12357789728873

# Tests
assert part_1(TEST_FILE_1) == 6
assert part_2(TEST_FILE_2) == 6
