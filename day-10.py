from copy import deepcopy
from pprint import pprint
from utils import profiler, get_lines


def char_to_directions(line: str) -> list[tuple[int, int, int, int]]:
    directions = {
        # c: (n, s, w, e)
        '|': (1, 1, 0, 0),
        '-': (0, 0, 1, 1),
        'L': (1, 0, 0, 1),
        'J': (1, 0, 1, 0),
        '7': (0, 1, 1, 0),
        'F': (0, 1, 0, 1),
        'S': (1, 1, 1, 1),
        '.': (0, 0, 0, 0),
    }

    return list(map(lambda x: directions[x], list(line)))


def get_pipes_matrix() -> list[list[tuple[int, int, int, int]]]:
    return list(map(char_to_directions, get_lines(__file__)))


def get_start_i_j(pipes: list[list[tuple[int, int, int, int]]]) -> (int, int):
    i = 0
    j = 0
    found_start = False
    while i < len(pipes) and not found_start:
        while j < len(pipes[0]) and not found_start:
            if pipes[i][j] == (0, 0, 0, 0):
                found_start = True
            j += 1
        i += 1
    return (i, j)


# TODO: wtf???
def create_graph(start_index: tuple[int, int], pipes: list[list[tuple[int, int, int, int]]]) -> dict[str, str]:
    graph: dict[str, str] = {}
    (i, j) = start_index

    start = pipes[i][j]
    curr = start
    curr_index = (i, j)
    prev_index = deepcopy(curr_index)
    counter = 0
    while not (curr is start and counter > 0):
        for (k, o) in enumerate(curr):
            if o == 0:
                continue

            match k:
                case 0:
                    new_i = i - o
                    if new_i >= 0 and pipes[new_i][j][k + 1] == 1:
                        curr = pipes[new_i][j]
                        i = new_i
                        break
                case 1:
                    new_i = i + o
                    if new_i < len(pipes) and pipes[new_i][j][k - 1] == 1:
                        curr = pipes[new_i][j]
                        i = new_i
                        break
                case 2:
                    new_j = j - o
                    if new_j >= 0 and pipes[i][new_j][k + 1] == 1:
                        curr = pipes[i][new_j]
                        j = new_j
                        break
                case 3:
                    new_j = j + o
                    if new_j < len(pipes[0]) and pipes[i][new_j][k - 1] == 1:
                        curr = pipes[i][new_j]
                        j = new_j
                        break

        prev_index = deepcopy(curr_index)
        curr_index = (i, j)
        graph[f'{prev_index}'] = f'{curr_index}'
        counter += 1

    return graph


@profiler
def part_one():
    pipes = get_pipes_matrix()
    graph = create_graph(get_start_i_j(pipes), pipes)
    pprint(graph)


@profiler
def part_two():
    pass


part_one()
part_two()
