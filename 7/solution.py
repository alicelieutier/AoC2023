#! /usr/bin/env python3
import os
import re
from math import sqrt, ceil, floor
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_hand(line):
  hand, bid = line.split()
  return hand, int(bid)

def parse_file(file):
  with open(file) as input:
    return [parse_hand(line.strip()) for line in input.readlines()]

ORDER = '23456789TJQKA'
def lexico_key(hand):
  hand, _ = hand
  return tuple(ORDER.index(letter) for letter in hand)

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456
def type_key(hand):
  hand, _ = hand
  counter = {card: 0 for card in set(hand)}
  for card in hand: counter[card] += 1
  match tuple(sorted(counter.values())):
    case 1,1,1,1,1: return 1
    case 1,1,1,2: return 2
    case 1,2,2: return 3
    case 1,1,3: return 4
    case 2,3: return 5
    case 1,4: return 6
    case (5,): return 7
    case _: print(f"Help! couldn't score hand: {hand, counter, tuple(sorted(counter.values()))}")

def part_1(file):
  hands = parse_file(file)
  hands.sort(key=lexico_key)
  hands.sort(key=type_key)
  return sum((index+1) * bid for index, (_, bid) in enumerate(hands))

# Solution
print(part_1(INPUT_FILE)) # 251058093

# Tests
assert part_1(TEST_FILE) == 6440
