class BettingLogic:
    def __init__(self, game):
        self.game = game
        self.raise_amt = 0
        self.player_ind = 1
        self.player_round_start = 0
    
    def betting_round(self, preFlop):
        if preFlop:
            # Small Blind
            # Big blind
            
            print("\n\n")
            print("Pre flop betting round -> ")
            ind = 0
            while not self.betting_finished():
                self.player_ind = (ind) % self.game.num_players
                
                if self.game.players[self.player_ind].fold:
                    print(f"Player {self.player_ind + 1} is folded...")
                    ind += 1
                    continue
                
                if self.game.players[self.player_ind].eliminated:
                    print(f"Player {self.player_ind + 1} is already eliminated...")
                    ind += 1
                    continue
                
                if self.game.players[self.player_ind].all_in:
                    print(f"Player {self.player_ind + 1} is all in!")
                    ind += 1
                    continue
                
                player_money_left = self.game.players[self.player_ind].curr_money_left
                player_decision, bet_amt = self.get_action(player_money_left)
                
                try:
                    self.bet_chosen(player_decision, bet_amt, ind)
                    ind += 1
                except Exception as e:
                    continue
            
            print("All bets accounted for! Let's play!")
                
    def get_action(self, player_money_left):
        print(f"Player {self.player_ind} (Current Balance = { player_money_left }): ")
                        
        print(f"""Choose 1 of the following:\n1) Call\n2) Raise\n3) Fold\n4) All In""")
        while True:
            try:
                player_decision = int(input("Your choice: "))
                break
            except Exception as e:
                print("Enter a valid input.")
                continue
        
        bet_amt = 0
        # Raise
        if player_decision == 2:
            while True:
                try:
                    bet_amt = int(input(f"Enter raise amount ( > {self.raise_amt}): "))
                    if bet_amt <= self.raise_amt:
                        print("Bet amount has to be greater than raise amount!!")
                        continue
                    break
                except Exception as e:
                    print("Enter a valid input")
                    continue
            self.player_round_start = self.player_ind
        # All In
        elif player_decision == 4:
            self.player_round_start = self.player_ind
            bet_amt = self.game.players[self.player_ind].curr_money_left
        
        return player_decision, bet_amt
                
    def bet_chosen(self, player_decision, bet_amt, ind):
        # Call
        if player_decision == 1:
            amt = 0
            if self.raise_amt == 0:
                amt = self.game.big_blind
            else:
                amt = self.raise_amt - self.game.players[self.player_ind].curr_round_bet
                
            self.game.pot += amt
            self.game.players[self.player_ind].curr_money_left -= amt
            self.game.players[self.player_ind].curr_round_bet += amt
            return
        
        # Raise
        elif player_decision == 2:            
            self.game.pot += bet_amt
            self.raise_amt = bet_amt
            self.game.players[self.player_ind].curr_money_left -= bet_amt
            return
        
        # Fold
        elif player_decision == 3:
            self.game.players[self.player_ind].fold = True
            self.game.players[self.player_ind].curr_round_bet = 0
            return

    def betting_finished(self):
        if self.player_ind == self.player_round_start:
            return True
