from typing import NamedTuple

class GameState(NamedTuple):
    state: str
    action: str

player_stack = 1000
small_blind = 1
big_blind = 2
fixed_raise = 10
pot = 0

def legal_actions(state):
    if state in ['Preflop', 'Raised']:
        return ['Fold', 'Call', 'Raise']
    else:
        return ['Fold', 'Check', 'Raise']

def apply_action(state, action):
    actions = legal_actions(state)
    if action not in actions:
        raise ValueError
    if action == 'Raise':
        pot += fixed_raise
        player_stack -= fixed_raise
        state = 'Raised'

    if action == 'Call':    
        pass

    if action == 'Fold':
        pass

    return GameState(action=action, state=state)



if __name__ == '__main__':
    game = GameState(state='Preflop', action='Call')
    print(apply_action(game.state, game.action))

class Game:
    def __init__(self, sb, bb, players):
        self.sb = small_blind
        self.bb = big_blind
        self.players = 2

    game = GameState(state='Preflop', action='')
    while game.state != 'Showdown': 
        
