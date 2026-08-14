import random
import math
def category_frequencies(trials, rng):
    from cards import shuffle_deck
    from evaluate import best_of_seven,evaluate_hand
    category_freq = {}
    for _ in range(trials):
        deal = shuffle_deck(rng)[0:7]
        hand, score = best_of_seven(deal[0:2], deal[2:])
        category_freq[evaluate_hand(hand)] = category_freq.get(evaluate_hand(hand), 0) + 1

    category_probablities = {category : (category_freq[category] / trials) for category in category_freq}
    return category_probablities
        

        
simulation_seed_1 = {'One Pair': 0.438232, 
                     'Flush': 0.030023999999999997, 
                     'Two Pair': 0.23396800000000002, 
                     'Straight': 0.046556, 
                     'Full House': 0.025976, 
                     'High Card': 0.174604, 
                     'Three of a Kind': 0.048515999999999995, 
                     'Four of a Kind': 0.001808, 
                     'Straight Flush': 0.000272, 
                     'Royal Flush': 0.000044}
        
def standard_error(simulation_seed, number_of_trials):
    return {category: math.sqrt(abs(simulation_seed[category] * (1 - simulation_seed[category]) / number_of_trials)) for category in simulation_seed}

print(standard_error(category_frequencies(50, random.Random(1)), 50))
        
def cannonical_hands(deck):
    cannonical_hands = []
    for i in range(len(deck)):
        for j in range(i + 1, len(deck)):
            cannonical_hands.append([deck[i], deck[j]])
    return cannonical_hands

def hand_in_label(deck):
    holes = cannonical_hands(deck)
    hole_labels = []
    for hole in holes:
        r1, r2 = hole[0].rank, hole[1].rank
        if r1 < r2:
            r1, r2 = r2, r1

        if hole[0].rank == hole[1].rank:
            label = f"{r1}{r2}"
            if label not in hole_labels:
                hole_labels.append(label)

        elif hole[0].suit == hole[1].suit:
            label = f"{r1}{r2}s"
            if label not in hole_labels:
                hole_labels.append(label)

        else:
            label = f"{r1}{r2}o"
            if label not in hole_labels:
                hole_labels.append(label)

    return hole_labels

def hand_equity(hole, trials, rng=random.Random(42)):
    from cards import shuffle_deck
    from evaluate import best_of_seven
    wins = 0
    ties = 0
    losses = 0
    for _ in range(trials):
        deck = shuffle_deck(rng)
        deck = [card for card in deck if card not in hole]
        opponent_hole = deck[:2]
        deck = deck[2:]
        community_cards = deck[:5]
        player_hand, player_score = best_of_seven(hole, community_cards)
        opponent_hand, opponent_score = best_of_seven(opponent_hole, community_cards)

        if player_score > opponent_score:
            wins += 1
        elif player_score == opponent_score:
            from evaluate import compare_equal_hands
            comparison = compare_equal_hands(player_hand, opponent_hand)
            if comparison == player_hand:
                wins += 1
            elif comparison == opponent_hand:
                losses += 1
            else:
                ties += 1
        else:
            losses += 1
    
    return {'wins': wins / trials, 'ties': ties / trials, 'losses': losses / trials}


def create_hole_from_label(label):
    from cards import Card
    rank1, rank2 = label[0], label[1]
    if len(label) == 2:
        return [Card(rank1, 's'), Card(rank2, 'h')]
    elif label[2] == 's':
        return [Card(rank1, 's'), Card(rank2, 's')]
    else:
        return [Card(rank1, 's'), Card(rank2, 'h')]



if __name__ == '__main__':
    from simulate import hand_in_label, hand_equity, create_hole_from_label
    from cards import make_deck
    deck = make_deck()
    rng = random.Random(42)
    trials = 10
    labels = hand_in_label(deck)
    equities = {label: hand_equity(create_hole_from_label(label), trials, rng) for label in labels}
    print(equities)




