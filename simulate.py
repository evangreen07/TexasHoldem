import random
def category_frequencies(trials, rng):
    from cards import shuffle_deck
    from evaluate import best_of_seven,evaluate_hand
    category_freq = {}
    for _ in range(trials):
        deal = shuffle_deck(rng)[0:7]
        hand, score = best_of_seven(deal[0:2], deal[2:])
        category_freq[evaluate_hand(hand)] = category_freq.get(evaluate_hand(hand), 0) + 1

    category_probablities = {category : 100 * (category_freq[category] / trials) for category in category_freq}
    return category_probablities
        

if __name__ == '__main__':
    print(category_frequencies(250000, random.Random(1)))
        
simulation_seed_1 = {'One Pair': 43.8232, 
                     'Flush': 3.0023999999999997, 
                     'Two Pair': 23.396800000000002, 
                     'Straight': 4.6556, 
                     'Full House': 2.5976, 
                     'High Card': 17.4604, 
                     'Three of a Kind': 4.8515999999999995, 
                     'Four of a Kind': 0.1808, 
                     'Straight Flush': 0.0272, 
                     'Royal Flush': 0.0044}
        

        








