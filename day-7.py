from itertools import combinations_with_replacement
from collections import Counter
from utils import get_lines, profiler


def get_hands_and_bids() -> list[tuple[str, int]]:
    hands_and_bids: list[tuple[str, int]] = []
    for line in get_lines(__file__):
        (hand, bid) = line.split(' ')
        hands_and_bids.append((hand, int(bid)))
    return hands_and_bids


def score_hand_strength_p1(hand: str) -> int:
    counts = {}
    for c in hand:
        counts[c] = counts.get(c, 0) + 1

    unique_cards = len(counts.keys())
    card_counts = set(counts.values())

    if 5 in card_counts:
        return 7
    elif 4 in card_counts:
        return 6
    elif 3 in card_counts:
        if 2 in card_counts:
            return 5
        return 4
    elif 2 in card_counts:
        if unique_cards == 3:
            return 3
        elif unique_cards == 4:
            return 2
    else:
        return 1


def score_cards_strength(hand: str, cards: list[str]) -> int:
    sum = 0
    for (index, card) in enumerate(hand):
        sum += (len(cards) - cards.index(card)) * \
            len(cards) ** (len(hand) - index)
    return sum


@profiler
def part_one():
    cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    hands_and_bids = get_hands_and_bids()
    scored_hands_and_bids = [[0, 0, hand, bid]
                             for (hand, bid) in hands_and_bids]

    for i in range(len(scored_hands_and_bids)):
        hand = scored_hands_and_bids[i][2]
        scored_hands_and_bids[i][0] = score_hand_strength_p1(hand)

    for i in range(len(scored_hands_and_bids)):
        hand = scored_hands_and_bids[i][2]
        scored_hands_and_bids[i][1] = score_cards_strength(hand, cards)

    scored_hands_and_bids.sort(key=lambda x: x[1])
    scored_hands_and_bids.sort(key=lambda x: x[0])

    bids_sum = 0
    for i in range(len(scored_hands_and_bids)):
        bids_sum += (i + 1) * scored_hands_and_bids[i][3]

    print(f'bids_sum: {bids_sum}')


def score_hand_strength_p2(hand: str) -> tuple[int, str]:
    counts = Counter(hand)

    if 'J' in counts:
        return score_with_jokers(hand, counts['J'])
    else:
        return score_without_jokers(counts), hand


def score_without_jokers(counts: Counter[str]) -> int:
    unique_cards = len(counts.keys())
    card_counts = set(counts.values())

    if 5 in card_counts:
        return 7
    elif 4 in card_counts:
        return 6
    elif 3 in card_counts:
        if 2 in card_counts:
            return 5
        return 4
    elif 2 in card_counts:
        if unique_cards == 3:
            return 3
        elif unique_cards == 4:
            return 2
    else:
        return 1


def compare_hands(hand1: str, hand2: str, cards: list[str]) -> bool:
    card_strength = {card: index for index, card in enumerate(cards)}
    for card1, card2 in zip(hand1, hand2):
        if card_strength[card1] != card_strength[card2]:
            return card_strength[card1] < card_strength[card2]
    return False  # hands are equal in strength


def score_with_jokers(hand: str, num_jokers: int) -> tuple[int, str]:
    max_score = 1
    best_hand = hand
    hand_without_jokers = [card for card in hand if card != 'J']
    cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

    for replacements in combinations_with_replacement(cards, num_jokers):
        new_counts = Counter(hand_without_jokers + list(replacements))
        score = score_without_jokers(new_counts)
        new_hand = ''.join(sorted(hand_without_jokers +
                           list(replacements), key=lambda x: cards.index(x)))
        if score > max_score or (score == max_score and compare_hands(new_hand, best_hand, cards)):
            max_score = score
            best_hand = new_hand

    return max_score, best_hand


@profiler
def part_two():
    cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    hands_and_bids = get_hands_and_bids()
    scored_hands_and_bids = [[0, 0, hand, bid]
                             for (hand, bid) in hands_and_bids]

    for i in range(len(scored_hands_and_bids)):
        hand = scored_hands_and_bids[i][2]
        (score, new_hand) = score_hand_strength_p2(hand)
        scored_hands_and_bids[i][0] = score
        scored_hands_and_bids[i].append(new_hand)

    for i in range(len(scored_hands_and_bids)):
        hand = scored_hands_and_bids[i][2]
        scored_hands_and_bids[i][1] = score_cards_strength(hand, cards)

    scored_hands_and_bids.sort(key=lambda x: x[1])
    scored_hands_and_bids.sort(key=lambda x: x[0])

    bids_sum = 0
    for i in range(len(scored_hands_and_bids)):
        bids_sum += (i + 1) * scored_hands_and_bids[i][3]

    print(f'bids_sum: {bids_sum}')


part_one()
part_two()
