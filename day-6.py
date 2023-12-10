from functools import reduce
from utils import profiler, get_lines


def get_line_vals(line: str) -> list[int]:
    return list(map(int, filter(lambda s: s != '', line.split(':')[1].split(' '))))


@profiler
def part_one():
    lines = get_lines(__file__)
    times = get_line_vals(lines[0])
    distances = get_line_vals(lines[1])

    ways_to_win_list: list[int] = []
    for (t, d) in zip(times, distances):
        ways_to_win = 0
        t_c = t // 2

        o = 0
        n_t_c = t_c - o
        c_d = (n_t_c) * (t - n_t_c)
        while c_d > d:
            ways_to_win += 1
            o += 1
            n_t_c = t_c - o
            c_d = (n_t_c) * (t - n_t_c)

        ways_to_win *= 2
        if t % 2 == 0:
            ways_to_win -= 1

        ways_to_win_list.append(ways_to_win)

    print(
        f'product_of_ways_to_win: {reduce(lambda acc, x: acc * x, ways_to_win_list, 1)}')


def get_val_from_line(line: str) -> int:
    return int(reduce(str.__add__, filter(lambda s: s != '' or s != ' ', line.split(':')[1].split()), ''))


# TODO: not optimal
@profiler
def part_two():
    lines = get_lines(__file__)
    t = get_val_from_line(lines[0])
    d = get_val_from_line(lines[1])

    ways_to_win = 0
    t_c = t // 2

    o = 0
    n_t_c = t_c - o
    c_d = (n_t_c) * (t - n_t_c)
    while c_d > d:
        ways_to_win += 1
        o += 1
        n_t_c = t_c - o
        c_d = (n_t_c) * (t - n_t_c)

    ways_to_win *= 2
    if t % 2 == 0:
        ways_to_win -= 1

    print(f'ways_to_win: {ways_to_win}')


part_one()
part_two()
