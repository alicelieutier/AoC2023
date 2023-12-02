#! /usr/bin/env python3
import os
import re
from collections import namedtuple
from functools import reduce

Game = namedtuple('Game', 'id red green blue')

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

# Returns a tuple representing the min number of red, green and blue cubes seen in a game
def minimum_color_cubes(game_str):
  color_cubes = re.split('[,;] ', game_str)

  def aux(acc, el):
    red, green, blue = acc
    # each element is a string like "4 green" or "20 blue"
    number, color = el.split(' ')
    if color == 'red': return (max(red, int(number)), green, blue)
    if color == 'green': return (red, max(green, int(number)), blue)
    if color == 'blue': return (red, green, max(blue, int(number)))
    raise Exception(f'unknown color {color}')

  return reduce(aux, color_cubes, (0,0,0))

LINE_PATTERN = re.compile(r'^Game (?P<id>\d+): (?P<draws>.+)')

def to_game(line):
  match = LINE_PATTERN.search(line)
  id = int(match.group('id'))
  red, green, blue = minimum_color_cubes(match.group('draws'))
  return Game(id, red, green, blue)

# playable with only 12 red cubes, 13 green cubes, and 14 blue cubes
def is_possible(game):
  return game.red <= 12 and game.green <= 13 and game.blue <= 14

# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
def power(game):
  return game.red * game.green * game.blue

def part_1(file):
  with open(file) as input:
    games = (to_game(line.strip()) for line in input.readlines())
    possible_games = list(filter(lambda game: is_possible(game), games))
    return sum(game.id for game in possible_games)
  
def part_2(file):
  with open(file) as input:
    games = (to_game(line.strip()) for line in input.readlines())
    return sum(power(game) for game in games)

# Solution
print(part_1(INPUT_FILE)) # 2006
print(part_2(INPUT_FILE)) # 84911

# Tests
assert part_1(TEST_FILE) == 8
assert part_2(TEST_FILE) == 2286
