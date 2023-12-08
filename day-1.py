from utils import get_lines, clear_log, log, profiler


def digit_match(a: str, b: str) -> int:
    for i in range(len(a)):
        if a[i] != b[i]:
            return 0
    return 1 + len(a) // len(b)

@profiler
def part_one():
    nums_sum = 0
    for line in get_lines(__file__):
        nums_list = list(filter(lambda char: char.isdigit(), line))
        nums_sum += int(''.join([nums_list[0], nums_list[len(nums_list) - 1]]))
    print(f'nums_sum: {nums_sum}')


def get_first_and_last_digit(line: str) -> list[str]:
    str_digits = {'one': '1', 'two': '2', 'three': '3', 'four': '4',
                  'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

    found_digits: list[tuple[str, int]] = []
    for key in str_digits.keys():
        last_index = 0
        while last_index != -1:
            index = line.find(key, last_index)
            if index >= 0:
                found_digits.append((str_digits[key], index))
                last_index = index + 1
            else:
                last_index = index

    for (index, c) in enumerate(line):
        if c.isdigit():
            found_digits.append((c, index))

    found_digits = sorted(found_digits, key=lambda x: x[1])

    return [found_digits[0][0], found_digits[len(found_digits) - 1][0]]

@profiler
def part_two():
    clear_log()

    nums_sum = 0
    for line in get_lines(__file__):
        log(f"{'line'.ljust(10)}: {line}")

        num_str = ''.join(get_first_and_last_digit(line))
        nums_sum += int(num_str)

        log(f"{'num_str'.ljust(10)}: '{num_str}'")
    print(f'nums_sum: {nums_sum}')


part_one()
part_two()
