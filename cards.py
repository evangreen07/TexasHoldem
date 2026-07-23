from typing import NamedTuple
class Card(NamedTuple):
    rank: str
    suit: str

def make_deck():
    ranks = [str(rank) for rank in range(2, 10)] + ["T", "J", "Q", "K", "A"]
    suits = ["s", "h", "d", "c"]
    return [Card(rank, suit) for suit in suits for rank in ranks]

def validate_card(card):
    valid_ranks = [str(rank) for rank in range(2, 10)] + ["T", "J", "Q", "K", "A"]
    valid_suits = ["s", "h", "d", "c"]
    if card.rank not in valid_ranks or card.suit not in valid_suits:
        raise ValueError(f"Invalid card: {card.rank} of {card.suit}")

def card_to_str(card):
    validate_card(card)
    return f"{card.rank}{card.suit}"


def str_to_card(text):
    if len(text) != 2 or text[0] not in [str(rank) for rank in range(2, 10)] + ["T", "J", "Q", "K", "A"] or text[1] not in ["s", "h", "d", "c"]:
        raise ValueError(f"Invalid card string: {text}")
    return Card(text[:-1], text[-1])
