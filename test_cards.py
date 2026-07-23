from cards import Card, card_to_str, make_deck, str_to_card, validate_card
import pytest

def test_card_round_trip_for_all_cards():
    for card in make_deck():
        assert str_to_card(card_to_str(card)) == card

def test_validate_card():
    validate_card(Card("A", "s"))
    validate_card(Card("T", "h"))
    validate_card(Card("5", "d"))
    validate_card(Card("K", "c"))
    with pytest.raises(ValueError) as e_info:
        validate_card(Card("2", "x"))
        assert str(e_info.value) == "Invalid card: 2 of x"

def test_card_to_str():
    assert card_to_str(Card("A", "s")) == "As"
    assert card_to_str(Card("T", "h")) == "Th"
    assert card_to_str(Card("5", "d")) == "5d"
    assert card_to_str(Card("K", "c")) == "Kc"

def test_str_to_card():
    assert str_to_card("As") == Card("A", "s")
    assert str_to_card("Th") == Card("T", "h")
    assert str_to_card("5d") == Card("5", "d")
    assert str_to_card("Kc") == Card("K", "c")
    with pytest.raises(ValueError) as e_info:
        str_to_card("2x")
        assert str(e_info.value) == "Invalid card string: 2x"

def test_make_deck():
    deck = make_deck()
    assert len(deck) == 52
    assert Card("A", "s") in deck
    assert Card("K", "c") in deck
    assert Card("2", "h") in deck
    assert Card("T", "d") in deck
    assert Card("J", "x") not in deck
    assert Card("1", "s") not in deck
    assert Card('', '') not in deck