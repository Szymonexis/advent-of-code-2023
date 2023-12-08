from typing import TypedDict, List
from utils import get_lines, profiler


class Scratchcard(TypedDict):
    winning_nums: list[int]
    my_nums: list[int]


class ScratchcardAmount(TypedDict):
    amount: int
    won_cards: list[int]


Scratchcards = List[Scratchcard]
ScratchcardAmounts = List[ScratchcardAmount]


def get_points(winning_nums: list[int], my_nums: list[int]) -> int:
    points = 0
    for w_num in winning_nums:
        for m_num in my_nums:
            if w_num == m_num:
                if points == 0:
                    points = 1
                else:
                    points *= 2

    return points


@profiler
def part_one():
    points_sum = 0
    for scratchcard in get_scratchcards():
        points_sum += get_points(scratchcard['winning_nums'],
                                 scratchcard['my_nums'])
    print(f'points_sum: {points_sum}')


def get_scratchcards() -> Scratchcards:
    scratchcards: Scratchcards = []
    for line in get_lines(__file__):
        line = line.strip()
        numbers = line.split(':')[1]
        [winning_nums, my_nums] = numbers.split('|')

        winning_nums = sorted(list(map(int, filter(lambda s: s != '', map(
            lambda s: s.strip(), winning_nums.split(' '))))))
        my_nums = sorted(list(map(int, filter(lambda s: s != '', map(
            lambda s: s.strip(), my_nums.split(' '))))))

        scratchcards.append(Scratchcard(
            winning_nums=winning_nums, my_nums=my_nums))
    return scratchcards


def get_matches(winning_nums: list[int], my_nums: list[int]) -> int:
    matches = 0
    for w_num in winning_nums:
        for m_num in my_nums:
            if w_num == m_num:
                matches += 1

    return matches


@profiler
def part_two():
    scratchcards = get_scratchcards()
    scratchcard_amounts: ScratchcardAmounts = list(
        map(lambda _: ScratchcardAmount(amount=1, won_cards=[]), scratchcards))

    for index in range(len(scratchcard_amounts)):
        scratchcard = scratchcards[index]
        matches = get_matches(
            scratchcard['winning_nums'], scratchcard['my_nums'])
        matches_list = list(range(matches))
        new_won_cards = map(lambda x: x + index + 1, matches_list)
        scratchcard_amounts[index]['won_cards'] = new_won_cards

    for index in range(len(scratchcard_amounts)):
        won_cards = scratchcard_amounts[index]['won_cards']
        for w_c_index in won_cards:
            scratchcard_amounts[w_c_index]['amount'] += scratchcard_amounts[index]['amount']

    counter = 0
    for index in range(len(scratchcard_amounts)):
        counter += scratchcard_amounts[index]['amount']

    print(f'counter: {counter}')


part_one()
part_two()
