from utils import profiler, get_lines


def get_histories() -> list[list[int]]:
    return [list(map(int, map(str.strip, s.split(' ')))) for s in get_lines(__file__)]


def get_history_differences(history: list[int]) -> (list[int], bool):
    all_zero = True
    differences: list[int] = []
    for i in range(len(history) - 1):
        l, r = (history[i], history[i+1])
        diff = r - l
        all_zero = all_zero and diff == 0
        differences.append(diff)
    return (differences, all_zero)


def extrapolate_history(history: list[int]) -> int:
    histories: list[list[int]] = [history]

    i = 0
    all_zeros = False
    while not all_zeros:
        (new_history, all_zeros) = get_history_differences(histories[i])
        i += 1
        histories.append(new_history)

    while i > 0:
        diffs = histories[i]
        target = histories[i - 1]
        histories[i - 1].append(target[len(target) - 1] +
                                diffs[len(diffs) - 1])
        i -= 1

    return histories[0][::-1][0]


@profiler
def part_one():
    sum_of_extrapolations = sum(map(extrapolate_history, get_histories()))
    print(f'sum_of_extrapolations: {sum_of_extrapolations}')


@profiler
def part_two():
    sum_of_extrapolations = sum(
        map(extrapolate_history, map(lambda x: list(reversed(x)), get_histories())))
    print(f'sum_of_extrapolations: {sum_of_extrapolations}')


part_one()
part_two()
