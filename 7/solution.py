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
  
def lexico_key(order):
  def aux(hand):
    hand, _ = hand
    return tuple(order.index(letter) for letter in hand)
  return aux

def hand_value(cards):
  counter = {card: 0 for card in set(cards)}
  for card in cards:
    counter[card] += 1
  match tuple(sorted(counter.values())):
    case 1,1,1,1,1: return 1 # High card
    case 1,1,1,2: return 2 # One pair
    case 1,2,2: return 3 # Two pair
    case 1,1,3: return 4 # Three of a kind
    case 2,3: return 5 # Full house
    case 1,4: return 6 # Four of a kind
    case (5,): return 7 # Five of a kind
    case _: print(f"Help! couldn't score hand: {cards, counter, tuple(sorted(counter.values()))}")

def type_key(hand):
  cards, _ = hand
  return hand_value(cards)

def type_key_with_joker(hand):
  cards, _ = hand
  if 'J' not in cards: return hand_value(cards)

  other_cards = {card for card in cards if card != 'J'}
  match len(other_cards):
    case 4: return 2 # One pair
    case 3: return 4 # Three of a kind
    case 2: # could result in a full house or a four of a kind
      if cards.count('J') == 1:
        return 5 if hand_value(cards) == 3 else 6
      return 6
    case _:
      return 7 # Five of a kind

assert(type_key_with_joker(('4QT44',0))) == 4 # Three of a kind
assert(type_key_with_joker(('2JQKA',0))) == 2 # One Pair
assert(type_key_with_joker(('96A89',0))) == 2 # One Pair
assert(type_key_with_joker(('QQQJA',0))) == 6 # Four of a kind
assert(type_key_with_joker(('QQJJA',0))) == 6 # Four of a kind
assert(type_key_with_joker(('235JA',0))) == 2 # One pair
assert(type_key_with_joker(('23JAA',0))) == 4 # Three of a kind
assert(type_key_with_joker(('QJ4J8',0))) == 4 # Three of a kind
assert(type_key_with_joker(('22JAA',0))) == 5 # Full house
assert(type_key_with_joker(('QQQJJ',0))) == 7 # Five of a kind
assert(type_key_with_joker(('JJJJJ',0))) == 7 # Five of a kind
assert(type_key_with_joker(('23JJJ',0))) == 6 # Four of a kind
assert(type_key_with_joker(('2222J',0))) == 7 # Five of a kind
assert(type_key_with_joker(('2J22J',0))) == 7 # Five of a kind

def part_1(file):
  hands = parse_file(file)
  hands.sort(key=lexico_key('23456789TJQKA'))
  hands.sort(key=type_key)
  return sum((index+1) * bid for index, (_, bid) in enumerate(hands))

def part_2(file):
  hands = parse_file(file)
  hands.sort(key=lexico_key('J23456789TQKA'))
  hands.sort(key=type_key_with_joker)
  return sum((index+1) * bid for index, (_, bid) in enumerate(hands))

# Solution
print(part_1(INPUT_FILE)) # 251058093
print(part_2(INPUT_FILE)) # 249781879

# Tests
assert part_1(TEST_FILE) == 6440
assert part_2(TEST_FILE) == 5905
