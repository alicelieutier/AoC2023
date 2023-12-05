#! /usr/bin/env python3
import os
import re
from functools import reduce
from itertools import batched

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_space_separated_numbers(string):
  return [int(number) for number in re.findall(r'(\d+)', string)]

def parse_section(section):
  lines = section.splitlines()
  name = tuple(lines[0].split()[0].split('-to-'))
  ranges = [tuple(parse_space_separated_numbers(line)) for line in lines[1:]]
  return name, ranges

def parse_file(file):
  with open(file) as input:
    sections = input.read().split('\n\n')
    seeds = parse_space_separated_numbers(sections[0])
    return seeds, [parse_section(section) for section in sections[1:]]

def is_in_range(number, range):
  _, source_start, length = range
  return number > source_start and number < source_start + length

def transform(number, range):
  dest_start, source_start, length = range
  return dest_start + (number - source_start)

def process_seed(sections, seed):
  def aux(seed, section):
    name, ranges = section
    for transformation_range in ranges:
      if is_in_range(seed, transformation_range):
        return transform(seed, transformation_range)
    return seed
  return reduce(aux, sections, seed)

def overlaps(range1, range2):
  if range1 > range2:
    range2, range1 = range1, range2
  s1,l1 = range1
  s2,l2 = range2
  return s1+l1 > s2

assert overlaps((6,1),(5,3)) == True
assert overlaps((6,1),(5,1)) == False
assert overlaps((2,4),(6,7)) == False
assert overlaps((2,6),(4,2)) == True

def intersection(range1, range2):
  if not overlaps(range1, range2): raise Exception(f'{range1} and {range2} do not overlap')
  if range1 > range2:
    range2, range1 = range1, range2
  s1,l1 = range1
  s2,l2 = range2
  return s2, min(s1+l1, s2+l2) - s2

assert intersection((2,6),(4,2)) == (4,2)
assert intersection((2,6),(2,6)) == (2,6)
assert intersection((7,3),(2,6)) == (7,1)

def leftover(range1, range2):
  if not overlaps(range1, range2): raise Exception(f'{range1} and {range2} do not overlap')
  s1,l1 = range1
  s2,l2 = range2
  result = []
  if s1 < s2: result.append((s1,s2-s1))
  if s1+l1 > s2+l2: result.append((s2+l2, s1+l1-s2-l2))
  return result

# returns an array of transformed ranges and an array of thing that are not in range
# for one seed range
def transform_range(seed_range, transformation_range):
  _, source_start, length = transformation_range
  t_range = source_start, length
  if not overlaps(seed_range, t_range):
    return [], [seed_range]
  # they overlap - we need to transform the intersection
  s, l = intersection(seed_range, t_range)
  return [(transform(s, transformation_range),l)], leftover(seed_range, t_range)

# processes all seed ranges into a transformation range
def process_one_transformation(seed_ranges, transformation_range):
  transformed, todo = seed_ranges
  all_leftover = []
  for seed_range in todo:
    t, leftover = transform_range(seed_range, transformation_range)
    transformed.extend(t)
    all_leftover.extend(leftover)
  return transformed, all_leftover
    
# Processes all seed ranges through a section    
def process_section(seed_ranges, section):
  name, ranges = section
  transformed, unchanged = reduce(process_one_transformation, ranges, ([], seed_ranges))
  return transformed + unchanged

def part_1(file):
  seeds, sections = parse_file(file)
  locations = [process_seed(sections, seed) for seed in seeds]
  return min(locations)

def part_2(file):
  seeds, sections = parse_file(file)
  location_ranges = reduce(process_section, sections, tuple(batched(seeds,2)))
  return min(location_ranges)[0]
  

# Solution
print(part_1(INPUT_FILE))
print(part_2(INPUT_FILE)) # 50716416

# Tests
assert part_1(TEST_FILE) == 35
assert part_2(TEST_FILE) == 46

