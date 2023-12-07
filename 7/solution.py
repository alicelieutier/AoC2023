#! /usr/bin/env python3
import os
import re

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  hand, bid = line.split()
  return hand, int(bid)

def parse_file(file):
  with open(file) as input:
    return [parse_line(line.strip()) for line in input.readlines()]

def lexico_key(alphabet):
  def aux(hand):
    hand, _ = hand
    return tuple(alphabet.index(letter) for letter in hand)
  return aux

# Card Frequencies:
# 1,1,1,1,1  High card
# 2,1,1,1    One pair
# 2,2,1      Two pair
# 3,1,1,1    Three of a kind
# 3,2        Full house
# 4,1        Four of a kind
# 5          Five of a kind

def hand_type_key(hand):
  cards, _ = hand
  counter = {card: cards.count(card) for card in cards}
  return sorted(counter.values(), reverse=True)

def hand_type_key_with_joker(hand):
  cards, _ = hand
  counter = {card: cards.count(card) for card in cards}
  if counter.get('J', 0) == 5:
    return [5]
  most_common_non_joker_card = sorted(cards, key=lambda card: 0 if card == 'J' else counter[card])[-1]
  counter[most_common_non_joker_card] += counter.pop('J', 0)
  return sorted(counter.values(), reverse=True)

def part_1(file):
  hands = parse_file(file)
  hands.sort(key=lexico_key('23456789TJQKA'))
  hands.sort(key=hand_type_key)
  return sum((index + 1) * bid for index, (_, bid) in enumerate(hands))

def part_2(file):
  hands = parse_file(file)
  hands.sort(key=lexico_key('J23456789TQKA'))
  hands.sort(key=hand_type_key_with_joker)
  return sum((index + 1) * bid for index, (_, bid) in enumerate(hands))

# Solution
print(part_1(INPUT_FILE)) # 251058093
print(part_2(INPUT_FILE)) # 249781879

# Tests
assert part_1(TEST_FILE) == 6440
assert part_2(TEST_FILE) == 5905
