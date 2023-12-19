#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os
import re

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

# @cache
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

def part_1(file):
  workflows, parts = parse_file(file)
  good_parts = filter(lambda part: is_accepted(workflows, part), parts)
  return sum(sum(part) for part in good_parts)

# Solution
print(part_1(INPUT_FILE))

# Tests
assert part_1(TEST_FILE) == 19114

assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,0,0,0)) == 'qkq'
assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,3000,3000,0)) == 'A'
assert workflow_result(('a<2006:qkq', 'm>2090:A', 'rfg'), (0,0,3000,0)) == 'rfg'
