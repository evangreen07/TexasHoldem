from cards import Card, card_to_str, make_deck, shuffle_deck, str_to_card, validate_card, shuffle_deck
from evaluate import compare_equal_hands, compare_full_houses, evaluate_hand, score_hand
import pytest
import random
import cards

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


def test_shuffle_deck_same_seed():
    rng = random.Random(42)
    deck_a = shuffle_deck(rng)
    rng = random.Random(42)
    deck_b = shuffle_deck(rng)
    assert deck_a == deck_b
    assert deck_a != make_deck()
    assert deck_b != make_deck()
    assert len(deck_a) == 52
    assert len(deck_b) == 52

def test_shuffle_deck_different_seeds():
    rng1 = random.Random(42)
    rng2 = random.Random(123)
    deck_a = shuffle_deck(rng1)
    deck_b = shuffle_deck(rng2)
    assert deck_a != deck_b
    assert deck_a != make_deck()
    assert deck_b != make_deck()
    assert len(deck_a) == 52
    assert len(deck_b) == 52

def test_main():
    from cards import __main__
    __main__()
    assert True

def test_main_with_different_player_count():
    from cards import __main__
    __main__(players=4)
    assert True

def test_main_with_maximum_players():
    from cards import __main__
    __main__(players=9)
    assert True

def test_main_with_different_seed():
    from cards import __main__
    dealing_hands = __main__(players=4)
    rng = random.Random(123)
    dealing_hands_2 = __main__(players=4, rng=rng)
    assert dealing_hands is not None
    assert len(dealing_hands) == 5
    assert len(dealing_hands[0]) == 2
    assert len(dealing_hands[1]) == 2
    assert len(dealing_hands[2]) == 2
    assert len(dealing_hands[3]) == 2
    assert len(dealing_hands[4]) == 5
    assert dealing_hands != dealing_hands_2

def test_main_with_same_seed():
    from cards import __main__
    rng = random.Random(42)
    dealing_hands = __main__(players=4, rng=rng)
    rng = random.Random(42)
    dealing_hands_2 = __main__(players=4, rng=rng)
    assert dealing_hands is not None
    assert len(dealing_hands) == 5
    assert len(dealing_hands[0]) == 2
    assert len(dealing_hands[1]) == 2
    assert len(dealing_hands[2]) == 2
    assert len(dealing_hands[3]) == 2
    assert len(dealing_hands[4]) == 5
    assert dealing_hands == dealing_hands_2


def test_main_with_invalid_player_count():
    from cards import __main__
    with pytest.raises(ValueError) as e_info:
        __main__(players=0)
    assert str(e_info.value) == "Number of players must be between 2 and 9."
    with pytest.raises(ValueError) as e_info:
        __main__(players=-1)
    assert str(e_info.value) == "Number of players must be between 2 and 9."
    with pytest.raises(ValueError) as e_info:
        __main__(players=10)
    assert str(e_info.value) == "Number of players must be between 2 and 9."

def test_check_no_duplicate_in_hands_and_community():
    from cards import __main__
    dealing_hands = __main__(players=4)
    all_cards = [card for hand in dealing_hands for card in hand]
    assert len(all_cards) == len(set(all_cards))

def test_check_for_royal_flush():
    hand = [Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "h"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Royal Flush"

def test_check_for_non_royal_flush():
    hand = [Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "h"), Card("9", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Royal Flush"
    hand_2 = [Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "d"), Card("A", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Royal Flush"

def test_check_for_straight_flush():
    hand = [Card("9", "h"), Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Straight Flush"

def test_check_for_non_straight_flush():
    hand = [Card("9", "h"), Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Straight Flush"
    hand_2 = [Card("9", "h"), Card("T", "h"), Card("J", "h"), Card("Q", "h"), Card("K", "d")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Straight Flush"

def test_check_for_four_of_a_kind():
    hand = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("9", "c"), Card("K", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Four of a Kind"

def test_check_for_non_four_of_a_kind():
    hand = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("K", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Four of a Kind"
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("9", "c"), Card("K", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Four of a Kind"

def test_check_for_full_house():
    hand = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("K", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Full House"

def test_check_for_non_full_house():
    hand = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("K", "c"), Card("K", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Full House"
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("8", "c"), Card("K", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Full House"

def test_check_for_flush():
    hand = [Card("2", "h"), Card("5", "h"), Card("9", "h"), Card("K", "h"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Flush"

def test_check_for_non_flush():
    hand = [Card("2", "h"), Card("5", "h"), Card("9", "h"), Card("K", "h"), Card("A", "d")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Flush"
    hand_2 = [Card("2", "h"), Card("5", "h"), Card("9", "d"), Card("K", "h"), Card("A", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Flush"

def test_check_for_three_of_a_kind():
    hand = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Three of a Kind"

def test_check_for_non_three_of_a_kind():
    hand = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("K", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Three of a Kind"
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("8", "c"), Card("A", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Three of a Kind"

def test_check_for_two_pair():
    hand = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("K", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "Two Pair"

def test_check_for_non_two_pair():
    hand = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("K", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "Two Pair"
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("7", "c"), Card("A", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "Two Pair"

def test_check_for_one_pair():
    hand = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "One Pair"

def test_check_for_non_one_pair():
    hand = [Card("9", "h"), Card("8", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "One Pair"
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("8", "s"), Card("8", "c"), Card("A", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "One Pair"

def test_check_for_high_card():
    hand = [Card("9", "h"), Card("8", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank == "High Card"

def test_check_for_non_high_card():
    hand = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand_rank = evaluate_hand(hand)
    assert hand_rank != "High Card"
    hand_2 = [Card("9", "h"), Card("J", "d"), Card("K", "s"), Card("Q", "c"), Card("T", "h")]
    hand_rank_2 = evaluate_hand(hand_2)
    assert hand_rank_2 != "High Card"

def test_check_hand_score():
    hand = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    score = score_hand(hand)
    assert score == 2  
    hand_2 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("K", "c"), Card("A", "h")]
    score_2 = score_hand(hand_2)
    assert score_2 == 3  
    hand_3 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("A", "h")]
    score_3 = score_hand(hand_3)
    assert score_3 == 4  
    hand_4 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("K", "h")]
    score_4 = score_hand(hand_4)
    assert score_4 == 7

def test_compare_hands():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "s"), Card("K", "c"), Card("A", "h")]
    score1 = score_hand(hand1)
    score2 = score_hand(hand2)
    assert score1 < score2

def test_compare_equal_hands():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    score1 = score_hand(hand1)
    score2 = score_hand(hand2)
    assert score1 == score2

def test_compare_equal_hands_with_kickers():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "s"), Card("J", "c"), Card("A", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_compare_equal_hands_full_house():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("A", "s"), Card("A", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "s"), Card("K", "d"), Card("K", "h")]
    winning_hand = compare_full_houses(hand1, hand2)
    assert winning_hand == hand1
    hand3 = [Card("A", "h"), Card("A", "d"), Card("2", "s"), Card("2", "c"), Card("2", "h")]
    hand4 = [Card("4", "s"), Card("4", "c"), Card("4", "s"), Card("K", "d"), Card("K", "h")]
    winning_hand_2 = compare_full_houses(hand3, hand4)
    assert winning_hand_2 == hand4

def test_compare_straight_flush_with_ace_low():
    hand1 = [Card("A", "h"), Card("2", "h"), Card("3", "h"), Card("4", "h"), Card("5", "h")]
    hand2 = [Card("2", "s"), Card("3", "s"), Card("4", "s"), Card("5", "s"), Card("6", "s")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand2

def test_compare_four_of_a_kind_with_kickers():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("9", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("9", "d"), Card("9", "h"), Card("K", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_compare_four_of_a_kind_with_kickers_low():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("9", "c"), Card("4", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("9", "d"), Card("9", "h"), Card("2", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_compare_flushes():
    hand1 = [Card("2", "h"), Card("5", "h"), Card("9", "h"), Card("K", "h"), Card("A", "h")]
    hand2 = [Card("3", "s"), Card("6", "s"), Card("9", "s"), Card("K", "s"), Card("A", "s")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand2

def test_three_of_a_kind_with_kickers():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("K", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("9", "d"), Card("Q", "c"), Card("A", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_three_of_a_kind_with_kickers_low():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("9", "s"), Card("4", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("9", "d"), Card("2", "c"), Card("K", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_two_pair_with_kickers():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("K", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "d"), Card("K", "h"), Card("Q", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_two_pair_with_kickers_low():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("K", "c"), Card("4", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "d"), Card("K", "h"), Card("2", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_one_pair_with_kickers():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("T", "d"), Card("4", "c"), Card("A", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_one_pair_with_kickers_low():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("4", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("T", "d"), Card("4", "c"), Card("2", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_high_card_with_kickers():
    hand1 = [Card("9", "h"), Card("8", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("8", "c"), Card("T", "d"), Card("4", "c"), Card("A", "h")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == hand1

def test_same_hand_comparison():
    hand1 = [Card("9", "h"), Card("8", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("8", "c"), Card("K", "d"), Card("Q", "h"), Card("A", "d")]
    winning_hand = compare_equal_hands(hand1, hand2)
    assert winning_hand == 0

def test_compare_different_hands():
    hand1 = [Card("9", "h"), Card("9", "d"), Card("K", "s"), Card("Q", "c"), Card("A", "h")]
    hand2 = [Card("9", "s"), Card("9", "c"), Card("K", "d"), Card("K", "h"), Card("A", "h")]
    with pytest.raises(ValueError) as e_info:
        compare_equal_hands(hand1, hand2)
        assert e_info.value == "Hands are not of the same rank."