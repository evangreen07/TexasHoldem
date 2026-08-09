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
        

if __name__ == '__main__':
    # print(category_frequencies(50, random.Random(1)))
    pass
        
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
        






