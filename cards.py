from typing import NamedTuple
import random

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
    return Card(text[0], text[1])

def shuffle_deck(rng):
    deck = make_deck()
    rng.shuffle(deck)
    return deck


def __main__(players=2, rng=random.Random(42)):
    if players < 2 or players > 9:
        raise ValueError("Number of players must be between 2 and 9.")
    shuffled_deck = shuffle_deck(rng)
    dealing_hands = [shuffled_deck[i*2:(i+1)*2] for i in range(players)] + [shuffled_deck[players*2:players*2+5]]
    for hand in dealing_hands[0:players]:
        print(f'Player Hand: {hand[0].rank}{hand[0].suit} {hand[1].rank}{hand[1].suit}')

    print(f'Community Cards: {" ".join(f"{card.rank}{card.suit}" for card in dealing_hands[-1])}')
    print(dealing_hands)
    return dealing_hands

if __name__ == "__main__":
    __main__()

