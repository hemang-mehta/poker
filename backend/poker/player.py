class Player:
    def __init__(self, id, name, money=10000, is_bot=False):
        self.player_id = id
        self.player_name = name
        self.player_ind = -1     
        self.curr_money_left = money
        self.is_bot = is_bot
        
        self.cards = []
        
        self.total_bet = 0
        self.curr_round_bet = 0 # the call/raise amount the player has irrespective of the call amount of the game
        self.all_in = False
        self.fold = False
        self.eliminated = False
        
        self.hand_rank = -1
        self.hand = []

class Bot(Player):

    def decide_action(self, game):
        # AI logic will go here
        pass