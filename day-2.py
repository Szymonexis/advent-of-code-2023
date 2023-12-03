import os

from utils import get_lines
from typing import TypedDict, List, Literal


class Cube(TypedDict):
    amount: int
    color: Literal['red', 'blue', 'green']


def get_game_id(line: str) -> int:
    return int(line[5:line.find(':')])


def map_str_to_cube(cube_str: str) -> Cube:
    cube_str_list = cube_str.split()
    return Cube(amount=int(cube_str_list[0]), color=cube_str_list[1])


def get_cubes(line: str) -> List[Cube]:
    line = line[line.find(':') + 1:]
    cubes_str = list(map(lambda s: s.strip(), line.split(',')))
    return list(map(map_str_to_cube, cubes_str))


def part_one():
    game_ids_sum = 0
    red_limit = 12
    green_limit = 13
    blue_limit = 14
    for line in get_lines(os.path.basename(__file__)):
        line = line.replace(';', ',')
        cubes = get_cubes(line)

        is_possible = True
        for cube in cubes:
            match cube['color']:
                case 'red':
                    if cube['amount'] > red_limit:
                        is_possible = False
                        break

                case 'green':
                    if cube['amount'] > green_limit:
                        is_possible = False
                        break

                case 'blue':
                    if cube['amount'] > blue_limit:
                        is_possible = False
                        break

        if is_possible:
            game_ids_sum += get_game_id(line)

    print(f'game_ids_sum: {game_ids_sum}')


def part_two():
    game_powers_sum = 0
    for line in get_lines(os.path.basename(__file__)):
        line = line.replace(';', ',')
        cubes = get_cubes(line)

        min_red = 0
        min_green = 0
        min_blue = 0
        for cube in cubes:
            match cube['color']:
                case 'red':
                    min_red = max(min_red, cube['amount'])
                case 'green':
                    min_green = max(min_green, cube['amount'])
                case 'blue':
                    min_blue = max(min_blue, cube['amount'])

        power = min_red * min_green * min_blue
        game_powers_sum += power

    print(f'game_powers_sum: {game_powers_sum}')


part_one()
part_two()
