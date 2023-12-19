from pprint import pprint
from utils import profiler, get_lines
import sys


OFFSETS: dict[str, tuple[int, int]] = {
    'n': (-1, 0),
    's': (1, 0),
    'w': (0, -1),
    'e': (0, 1),
}

OPPOSITES: dict[str, str] = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w',
}

GRAPH_NON_PATH = -2
GRAPH_PATH = 1
GRAPH_ENCLOSED = -1


Graph = list[list[int]]


def graph_path(v: int = GRAPH_PATH) -> int:
    return v


def line_to_directions(line: str) -> list[str]:
    directions = {
        '|': 'ns',
        '-': 'we',
        'L': 'ne',
        'J': 'nw',
        '7': 'ws',
        'F': 'es',
        'S': 'nswe',
        '.': '',
    }

    return list(map(lambda c: directions[c], list(line)))


def get_directions() -> list[list[str]]:
    return list(map(line_to_directions, get_lines(__file__)))


def get_graph_and_max_length() -> tuple[Graph, int]:
    opposites = OPPOSITES
    offsets = OFFSETS
    pipes = get_directions()
    graph: Graph = [[GRAPH_NON_PATH for _ in p] for p in pipes]

    # find start index
    i = 0
    j = 0
    start_index = ()
    while i < len(pipes) and start_index == ():
        j = 0
        while j < len(pipes[0]) and start_index == ():
            if pipes[i][j] == 'nswe':
                start_index = (i, j)
            j += 1
        i += 1

    # find length of the route
    (i, j) = start_index
    start = (i, j)
    prev_direction = ''
    counter = 0
    graph[i][j] = graph_path(counter)
    while (i, j) != start or prev_direction == '':
        if prev_direction == '':
            next_direction = ''
            for c in pipes[i][j]:
                offset = offsets[opposites[c]]
                next_direction = pipes[i + offset[0]][j + offset[1]]
                if next_direction.find(c) + 1:
                    prev_direction = opposites[c]
                    i += offset[0]
                    j += offset[1]
                    graph[i][j] = graph_path(counter)
                    counter += 1
                    break
        else:
            graph[i][j] = graph_path(counter)
            counter += 1
            prev_direction = next_direction.replace(
                opposites[prev_direction], '')
            offset = offsets[prev_direction]
            i += offset[0]
            j += offset[1]
            next_direction = pipes[i][j]

    max_length = counter // 2
    return (graph, max_length)


@profiler
def part_one():
    (_, max_length) = get_graph_and_max_length()
    print(f'max_length: {max_length}')


def mark_enclosed_areas(grid: Graph) -> Graph:
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and grid[x][y] == GRAPH_NON_PATH and not visited[x][y]

    def flood_fill(x, y):
        if not is_valid(x, y):
            return
        visited[x][y] = True
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            flood_fill(x + dx, y + dy)

    for i in range(rows):
        for j in range(cols):
            if i == 0 or j == 0 or i == rows - 1 or j == cols - 1:
                flood_fill(i, j)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == GRAPH_NON_PATH and not visited[i][j]:
                grid[i][j] = GRAPH_ENCLOSED

    return grid


def count_enclosed(graph: Graph) -> int:
    counter = 0
    for r in graph:
        for v in r:
            if v == GRAPH_ENCLOSED:
                counter += 1
    return counter


def double_resolution(graph: Graph) -> Graph:
    doubled_res_graph = [[GRAPH_NON_PATH for _ in range(
        len(graph[0]) * 2)] for _ in range(len(graph) * 2)]
    i = 0
    j = 0
    while i < len(graph):
        j = 0
        while j < len(graph[0]):
            v = graph[i][j]
            d_i = i * 2
            d_j = j * 2
            doubled_res_graph[d_i][d_j] = v
            j += 1
        i += 1
    return doubled_res_graph


def half_resolution(graph: Graph) -> Graph:
    half_res_graph = [[GRAPH_NON_PATH for _ in range(
        len(graph[0]) // 2)] for _ in range(len(graph) // 2)]

    i = 0
    j = 0
    while i < len(graph):
        j = 0
        while j < len(graph[0]):
            half_res_graph[i // 2][j // 2] = graph[i][j]
            j += 2
        i += 2
    return half_res_graph


# TODO: very cool, doesnt work
# https://www.reddit.com/r/adventofcode/comments/18fgddy/2023_day_10_part_2_using_a_rendering_algorithm_to/
@profiler
def part_two():
    (graph, _) = get_graph_and_max_length()
    double_res_graph = double_resolution(graph)
    # marked_enclosed = mark_enclosed_areas(double_res_graph)
    # marked_enclosed_graph = half_resolution(marked_enclosed)
    # tiles_num = count_enclosed(marked_enclosed_graph)
    # print(f'tiles_num: {tiles_num}')

    pprint(graph)
    pprint(double_res_graph)


part_one()
part_two()
