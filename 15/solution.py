#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_file(file):  
  with open(file) as input:
    return input.read().strip().split(',')

def hash_algorithm(string):
  current_value = 0
  for char in string:
    current_value += ord(char)
    current_value = (current_value * 17) % 256
  return current_value

# returns (label, op, focal_length)
# cm=4  becomes ('cm', '=', 4)
# bhg-  becomes ('bhg', '-', None)
def parse_step(step):
  if '=' in step:
    label, focal_length = step.split('=')
    return label, '=', int(focal_length)
  return step[:-1], '-', None

class Box:
  def __init__(self) -> None:
    self.lenses = []
    self.focals = {}

  def remove(self, label):
    if label in self.focals:
      self.lenses.remove(label)
      self.focals.pop(label)
  
  def place(self, label, focal_length):
    if label not in self.focals:
      self.lenses.append(label)
    self.focals[label] = focal_length

  def focusing_power(self, box_number):
    return sum((box_number + 1) * (i+1) * self.focals[label] for i, label in enumerate(self.lenses))

def hashmap(sequence):
  boxes = [Box() for _ in range(256)]
  for step in sequence:
    label, op, focal_length = parse_step(step)
    box = hash_algorithm(label)
    if op == '-':
      boxes[box].remove(label)
    if op == '=':
      boxes[box].place(label, focal_length)
  return boxes

def part_1(file):
  sequence = parse_file(file)
  return sum(hash_algorithm(step) for step in sequence)

def part_2(file):
  sequence = parse_file(file)
  boxes = hashmap(sequence)
  return sum(box.focusing_power(i) for i, box in enumerate(boxes))

# Solution
print(part_1(INPUT_FILE))
print(part_2(INPUT_FILE))

# Tests
assert hash_algorithm('HASH') == 52

assert(part_1(TEST_FILE)) == 1320
assert(part_2(TEST_FILE)) == 145
