class Player:
    def __init__(self, name, money=10000, is_bot=False):
        
        self.player_name = name        
        self.curr_money_left = money
        self.is_bot = is_bot
        
        self.cards = []
        
        self.total_bet = 0
        self.curr_round_bet = 0
        self.all_in = False
        self.fold = False
        self.eliminated = False
        
        self.hand_rank = -1
        self.hand = []

class Bot(Player):

    def decide_action(self, game_state):
        # AI logic will go here
        pass