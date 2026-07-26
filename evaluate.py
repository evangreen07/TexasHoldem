import itertools
from cards import Card

def evaluate_hand(hand):
    if is_royal_flush(hand):
        return "Royal Flush"

    if is_straight_flush(hand):
        return "Straight Flush"

    if is_four_of_a_kind(hand):
        return "Four of a Kind"

    if is_full_house(hand):
        return "Full House"

    if is_flush(hand):
        return "Flush"

    if is_straight(hand):
        return "Straight"

    if is_three_of_a_kind(hand):
        return "Three of a Kind"

    if is_two_pair(hand):
        return "Two Pair"

    if is_one_pair(hand):
        return "One Pair"   
    
    return "High Card"

def is_royal_flush(hand):
    if len(hand) != 5:
        return False
    suits = [card.suit for card in hand]
    ranks = [card.rank for card in hand]
    if len(set(suits)) != 1:
        return False
    rank_values = sorted([int(rank) if rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank] for rank in ranks])
    return all(rank_values[i] + 1 == rank_values[i + 1] for i in range(len(rank_values) - 1)) and rank_values[0] == 10

def is_straight_flush(hand):
    if len(hand) != 5:
        return False
    suits = [card.suit for card in hand]
    ranks = [card.rank for card in hand]
    if len(set(suits)) != 1:
        return False
    rank_values = sorted([int(rank) if rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank] for rank in ranks])
    if rank_values == [2, 3, 4, 5, 14]:
        return True
    return all(rank_values[i] + 1 == rank_values[i + 1] for i in range(len(rank_values) - 1)) and rank_values[0] != 10

def is_four_of_a_kind(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    return 4 in rank_counts.values()

def is_full_house(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    return sorted(rank_counts.values()) == [2, 3]

def is_flush(hand):
    if len(hand) != 5:
        return False
    suits = [card.suit for card in hand]
    return len(set(suits)) == 1

def is_straight(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_values = sorted([int(rank) if rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank] for rank in ranks])
    if rank_values == [2, 3, 4, 5, 14]:
        return True
    return all(rank_values[i] + 1 == rank_values[i + 1] for i in range(len(rank_values) - 1))

def is_three_of_a_kind(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    return 3 in rank_counts.values() and len(rank_counts) == 3

def is_two_pair(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    return list(rank_counts.values()).count(2) == 2

def is_one_pair(hand):
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    return list(rank_counts.values()).count(2) == 1

def score_hand(hand):
    rank_scores = {
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }
    return rank_scores[evaluate_hand(hand)]

def compare_equal_hands(hand1, hand2):
    rank1 = evaluate_hand(hand1)
    rank2 = evaluate_hand(hand2)
    
    if rank1 != rank2:
        raise ValueError("Hands are not of the same rank.")
     
    def get_rank_values(hand):
        return sorted([int(card.rank) if card.rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card.rank] for card in hand], reverse=True)

    values1 = get_rank_values(hand1)
    values2 = get_rank_values(hand2)

    if rank1 in ['Straight', 'Straight Flush']:
        if values1 == [14, 5, 4, 3, 2]:
            values1 = [5, 4, 3, 2, 1]
        if values2 == [14, 5, 4, 3, 2]:
            values2 = [5, 4, 3, 2, 1]

    if rank1 == 'Full House':
        return compare_full_houses(hand1, hand2)
    
    if values1 > values2:
        return hand1
    elif values1 < values2:
        return hand2
    else:
        return 0

def compare_full_houses(hand1, hand2):
    def get_full_house_values(hand):
        ranks = [card.rank for card in hand]
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        three_of_a_kind_rank = max(rank_counts, key=lambda rank: (rank_counts[rank], int(rank) if rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank]))
        pair_rank = min(rank_counts, key=lambda rank: (rank_counts[rank], int(rank) if rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank]))
        three_of_a_kind_value = int(three_of_a_kind_rank) if three_of_a_kind_rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[three_of_a_kind_rank]
        pair_value = int(pair_rank) if pair_rank.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[pair_rank]
        return (three_of_a_kind_value, pair_value)

    values1 = get_full_house_values(hand1)
    values2 = get_full_house_values(hand2)
    if values1 > values2:
        return hand1
    elif values1 < values2:
        return hand2
    else:
        return 0


def best_of_seven(hole_cards, community_cards):
    all_cards = hole_cards + community_cards
    all_hands = [(combination, score_hand(combination)) for combination in itertools.combinations(all_cards, 5)]
    if len(all_hands) != 21:
        raise ValueError("Not all combinations are valid.")

    highest = max(all_hands, key=lambda x: x[1])[1]
    best_hands = [hand for hand, score in all_hands if score == highest]
    highest_hand = None
    for hand in best_hands:
        if highest_hand is None:
            highest_hand = hand
        else:
            comparison = compare_equal_hands(highest_hand, hand)
            if comparison == hand:
                highest_hand = hand
            elif comparison == 0:
                continue

    return (highest_hand, score_hand(highest_hand))


def winners(hole1, hole2, community_cards):
    hand1, score1 = best_of_seven(hole1, community_cards)
    hand2, score2 = best_of_seven(hole2, community_cards)
    if score1 > score2:
        return ('Player 1', hand1)
    elif score1 < score2:
        return ('Player 2', hand2)
    else:
        comparison = compare_equal_hands(hand1, hand2)
        return ('Player 1', hand1) if comparison == hand1 else ('Player 2', hand2)

def format_output(hand, player='You', symbol=True):
    def utility(hand, symbol):
        if symbol:
            hand_output = ' '.join(card_to_str(card) for card in hand)
            return ''.join({'d': '♦', 's': '♠', 'c': '♣', 'h': '♥'}.get(card, card) for card in hand_output) 
           
        else:
            return ' '.join(card_to_str(card) for card in hand)
            

    from cards import card_to_str
    return f'{player} won with a {evaluate_hand(hand)}: {utility(hand, symbol)}'


if __name__ == '__main__':
    print(format_output([Card("A", "s"), Card("7", "h"), Card("T", "s"), Card("4", "d"), Card("Q", "h")], 'You'))