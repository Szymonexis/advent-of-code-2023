from typing import List
from utils import get_lines, profiler


Schematic = List[List[str]]


def is_symbol(s: str) -> bool:
    return not s.isdigit() and not s == '.'


def is_star(s: str) -> bool:
    return s == '*'


def get_schematic() -> Schematic:
    schematic: Schematic = []
    for line in get_lines(__file__):
        line = line.strip()
        schematic.append(list(line))
    return schematic


def get_adjecent_numbers(schematic: Schematic, x: int, y: int) -> list[int]:
    min_x = 0 if x - 1 < 0 else x - 1
    min_y = 0 if y - 1 < 0 else y - 1
    max_x = len(schematic) - 1 if x + 1 > len(schematic) - 1 else x + 1
    max_y = len(schematic[0]) - 1 if y + 1 > len(schematic[0]) - 1 else y + 1

    found_digits: list[tuple[int, int]] = []
    for t_x in range(min_x, max_x + 1):
        for t_y in range(min_y, max_y + 1):
            if t_x == x and t_y == y:
                continue

            if schematic[t_x][t_y].isdigit():
                found_digits.append((t_x, t_y))

    found_numbers_indexes: list[tuple[int, int, int]] = []
    for (f_x, f_y) in found_digits:
        go_left = True
        go_right = True
        left = f_y
        right = f_y
        while go_left or go_right:
            n_right = right + 1 if right + 1 < len(schematic[0]) else right
            n_left = left - 1 if left - 1 >= 0 else left

            if n_left == left:
                go_left = False

            if n_right == right:
                go_right = False

            if go_left and schematic[f_x][n_left].isdigit():
                left = n_left
            else:
                go_left = False

            if go_right and schematic[f_x][n_right].isdigit():
                right = n_right
            else:
                go_right = False

        found_numbers_indexes.append((f_x, left, right + 1))

    return list(map(lambda t: int(''.join(schematic[t[0]][t[1]:t[2]])), set(found_numbers_indexes)))


@profiler
def part_one():
    schematic = get_schematic()

    parts_sum = 0
    for x in range(len(schematic)):
        for y in range(len(schematic[0])):
            if is_symbol(schematic[x][y]):
                parts_sum += sum(get_adjecent_numbers(schematic, x, y))

    print(f'parts_sum: {parts_sum}')


@profiler
def part_two():
    schematic = get_schematic()

    gear_ratios_sum = 0
    for x in range(len(schematic)):
        for y in range(len(schematic[0])):
            if is_star(schematic[x][y]):
                nums = get_adjecent_numbers(schematic, x, y)

                if len(nums) == 2:
                    ratio = nums[0] * nums[1]
                    gear_ratios_sum += ratio

    print(f'gear_ratios_sum: {gear_ratios_sum}')


part_one()
part_two()
