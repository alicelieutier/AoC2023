#! /usr/bin/env python3
import os
import re
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_space_separated_numbers(string):
  return [int(number) for number in re.findall(r'(\d+)', string)]

def parse_section(section):
  lines = section.splitlines()
  name = lines[0].split()[0]
  ranges = [tuple(parse_space_separated_numbers(line)) for line in lines[1:]]
  return name, ranges

def parse_file(file):
  with open(file) as input:
    sections = input.read().split('\n\n')
    seeds = parse_space_separated_numbers(sections[0])
    return seeds, [parse_section(section) for section in sections[1:]]

def process_seed(sections, seed):
  def aux(seed, section):
    name, ranges = section
    for dest_range_start, source_range_start, range_length in ranges:
      if seed >= source_range_start and seed < source_range_start + range_length:
        return dest_range_start + (seed - source_range_start)
    return seed
  return reduce(aux, sections, seed)

def part_1(file):
  seeds, sections = parse_file(file)
  locations = [process_seed(sections, seed) for seed in seeds]
  return min(locations)

# Solution
print(part_1(INPUT_FILE))

# Tests
assert part_1(TEST_FILE) == 35
