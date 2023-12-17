from functools import reduce
from pprint import pprint
from utils import get_lines, profiler


def get_instructions(line: str) -> list[int]:
    instructions: list[int] = []
    for c in line:
        instructions.append(0 if c == 'L' else 1)
    return instructions


def get_graph(lines: list[str]) -> dict[str, tuple[str, str]]:
    graph = {}
    for line in lines:
        if not line:
            continue

        node, connections = line.split('=')
        node = node.strip()
        left_node, right_node = connections.strip().strip('()').split(',')
        left_node = left_node.strip()
        right_node = right_node.strip()
        graph[node] = (left_node, right_node)
    return graph


@profiler
def part_one():
    lines = get_lines(__file__)
    instructions = get_instructions(lines[0])
    graph = get_graph(lines[1:])

    target = 'AAA'
    i = 0
    steps = 0
    while target != 'ZZZ':
        target = graph[target][instructions[i]]
        i = (i + 1) % len(instructions)
        steps += 1

    print(f'steps: {steps}')


def find_start_nodes(graph: dict[str, tuple[str, str]]) -> list[str]:
    return list(filter(lambda s: s[2] == 'A', graph.keys()))


def check_if_all_targets_met(targets: list[str]) -> bool:
    return reduce(lambda acc, s: (acc and s[2] == 'Z'), targets, True)


# @TODO: Try to find all starting points and LCM ()
@profiler
def part_two():
    lines = get_lines(__file__)
    instructions = get_instructions(lines[0])
    graph = get_graph(lines[1:])
    start_nodes = find_start_nodes(graph)

    i = 0
    steps = 0

    print(f'steps: {steps}')


part_one()
part_two()
