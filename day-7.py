from utils import get_lines, profiler


def get_hands_and_bids() -> list[tuple[str, int]]:
    hands_and_bids: list[tuple[str, int]] = []
    for line in get_lines(__file__):
        (hand, bid) = line.split(' ')
        hands_and_bids.append((hand, int(bid)))
    return hands_and_bids


def classify_hand(hand: str) -> str:
    counts = {}
    for c in hand:
        counts[c] = counts.get(c, 0) + 1

    unique_cards = len(counts.keys())
    card_counts = set(counts.values())

    if 5 in card_counts:
        return 'Five of a Kind'
    elif 4 in card_counts:
        return 'Four of a Kind'
    elif 3 in card_counts:
        if 2 in card_counts:
            return 'Full House'
        return 'Three of a Kind'
    elif 2 in card_counts:
        if unique_cards == 3:
            return 'Two Pair'
        elif unique_cards == 4:
            return 'One Pair'
    else:
        return 'High Card'


@profiler
def part_one():
    hands_and_bids = get_hands_and_bids()
    cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    hand_types = ['Five of a kind', 'Four of a kind', 'Full house',
                  'Three of a kind', 'Two pair', 'One pair', 'High card']

    # hand_type_strength
    # pow(len(hand_types), 2) * (hand_types.find(hand_calssification) + 1)
    #
    # card_strength
    # len(cards) * (cards.find(card) + 1)



    pass


@profiler
def part_two():
    pass


part_one()
part_two()
