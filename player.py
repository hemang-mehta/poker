class Player:
    def __init__(self):
        self.curr_money_left = 10000
        
        self.cards = []
        
        self.total_bet = 0
        self.curr_round_bet = 0
        self.all_in = False
        self.fold = False
        self.eliminated = False
        
        self.hand_rank = -1
        self.hand = []