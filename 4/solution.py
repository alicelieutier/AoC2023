#! /usr/bin/env python3
import os
import re
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def to_card(line):
  match = re.search(r'Card +(\d+): ([0-9 ]+) \| ([0-9 ]+)', line)
  id, first_half, second_half = match.groups()
  winning = {int(number) for number in re.findall(r'(\d+)', first_half)}
  appeared = {int(number) for number in re.findall(r'(\d+)', second_half)}
  return int(id), winning, appeared

def parse_file(file):
  with open(file) as input:
    return [to_card(line.strip()) for line in input.readlines()]
  
def worth(card):
  _, winning, appeared = card
  nb_in_common = len(winning & appeared)
  if nb_in_common > 0:
    return 2**(nb_in_common - 1)
  return 0

def count_cards(cards):
  def aux(counter, card):
    id,  winning, appeared = card
    nb_in_common = len(winning & appeared)
    for i in range(id + 1, id + nb_in_common + 1):
      counter[i] += counter[id]
    return counter
  
  counter = reduce(aux, cards, {id: 1 for id, _ , _ in cards})
  return sum(counter.values())

def part_1(file):
  cards = parse_file(file)
  return sum(worth(card) for card in cards)

def part_2(file):
  cards = parse_file(file)
  return count_cards(cards)
  
# Solution
print(part_1(INPUT_FILE)) # 18619
print(part_2(INPUT_FILE)) # 8063216

# Tests
assert part_1(TEST_FILE) == 13
assert part_2(TEST_FILE) == 30

