#! /usr/bin/env python3
import os
import re
from collections import namedtuple

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

Game = namedtuple('Game', 'id red green blue')

def to_game(line):
  id = int(re.match(r'Game (\d+):', line).group(1))
  red = max(int(number) for number in re.findall(r'(\d+) red', line))
  green = max(int(number) for number in re.findall(r'(\d+) green', line))
  blue = max(int(number) for number in re.findall(r'(\d+) blue', line))
  return Game(id, red, green, blue)

def parse_file(file):
  with open(file) as input:
    return (to_game(line.strip()) for line in input.readlines())

# Is playable with only 12 red cubes, 13 green cubes, and 14 blue cubes
def is_possible(game):
  return game.red <= 12 and game.green <= 13 and game.blue <= 14

# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
def power(game):
  return game.red * game.green * game.blue

def part_1(file):
  games = parse_file(file)
  possible_games = filter(is_possible, games)
  return sum(game.id for game in possible_games)
  
def part_2(file):
  games = parse_file(file)
  return sum(power(game) for game in games)

# Solution
print(part_1(INPUT_FILE)) # 2006
print(part_2(INPUT_FILE)) # 84911

# Tests
assert part_1(TEST_FILE) == 8
assert part_2(TEST_FILE) == 2286
