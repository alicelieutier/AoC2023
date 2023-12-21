#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
import re
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_workflow(line):
  name, rules = re.match(r'^(?P<name>[a-z]+){(?P<rules>.+)}', line).groups()
  return name, tuple(rules.split(','))

def parse_part(line):
  numbers = re.findall(r'(\d+)', line)
  return tuple(int(number) for number in numbers)

def parse_file(file):  
  with open(file) as input:
    workflows, parts = input.read().split('\n\n')
    workflows = dict(parse_workflow(line) for line in workflows.splitlines())
    parts = [parse_part(line) for line in parts.splitlines()]
    return workflows, parts

def workflow_result(workflow, part) -> str:
  x,m,a,s = part
  for rule in workflow:
    if ':' not in rule:
      return rule
    cond, result = rule.split(':')
    if (eval(cond)):
      return result
    
def is_accepted(workflows, part) -> bool:
  current = 'in'
  while current := workflow_result(workflows[current], part):
    if current in 'RA':
      return True if current == 'A' else False


def product(numbers):
  return reduce(lambda x,y: x*y, numbers)

def count_parts(min_max):
  return product((max-min+1) for min, max in min_max.values()) 

# return interval that follows the rule, interval that doesn't
def split_values(min, max, symbol, value):
  if symbol == '<':
    if max < value:
      return (min,max), None
    if min >= value:
      return None, (min,max)
    return (min, value-1), (value, max)
  if symbol == '>':
    if max <= value:
      return None, (min,max)
    if min > value:
      return (min,max), None
    return (value+1, max), (min, value)

# {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
def number_accepted(workflows, min_max, workflow='in', rule_index=0):
  rule = workflows[workflow][rule_index]
  # simple rules
  if rule == 'R': return 0
  if rule == 'A': return count_parts(min_max)
  if ':' not in rule: return number_accepted(workflows, min_max, rule, 0)
  # complex rules
  var, number, consequence = re.split(r'[<>:]', rule)
  symbol = rule[1]
  minv, maxv = min_max[var]
  match split_values(minv, maxv, symbol, int(number)):
    case _, None:
      return number_accepted(workflows, min_max, workflow, rule_index+1)
    case None, _:
      if consequence == 'R': return 0
      if consequence == 'A': return count_parts(min_max)
      return number_accepted(workflows, min_max, consequence, 0)
    case left, right:
      min_max_left, min_max_right = min_max.copy(), min_max.copy()
      min_max_left[var], min_max_right[var] = left, right
      if consequence == 'R':
        return number_accepted(workflows, min_max_right, workflow, rule_index+1)
      if consequence == 'A':
        return count_parts(min_max_left) + number_accepted(workflows, min_max_right, workflow, rule_index+1)
      return number_accepted(workflows, min_max_left, consequence, 0) + number_accepted(workflows, min_max_right, workflow, rule_index+1)

def part_1(file):
  workflows, parts = parse_file(file)
  good_parts = filter(lambda part: is_accepted(workflows, part), parts)
  return sum(sum(part) for part in good_parts)

def part_2(file):
  workflows, _ = parse_file(file)
  min_max = {l:(1,4000) for l in 'xmas'}
  return number_accepted(workflows, min_max)  

# Solution
print(part_1(INPUT_FILE))
print(part_2(INPUT_FILE))

# Tests
assert part_1(TEST_FILE) == 19114
assert part_2(TEST_FILE) == 167409079868000

assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,0,0,0)) == 'qkq'
assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,3000,3000,0)) == 'A'
assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,0,3000,0)) == 'rfg'
