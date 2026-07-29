class Poker_Game:
    
    def __init__(self):
        import cards
        from collections import deque
        
        self.cards = cards.Cards()
        
        # Full Deck
        self.full_deck = self.cards.get_full_deck()
        self.full_deck = deque(self.full_deck)
        
        self.num_players = 3
        self.table_cards = []
        self.players = []
        self.pot = 0
        self.small_blind = 100
        self.big_blind = 200
    
    def play(self):
        import betting_logic
        import dealer
        
        # Shuffle Deck
        self.cards.shuffle_cards(self.full_deck)
        
        # Get Players
        self.create_players()
        
        main_dealer = dealer.Dealer(self)
        
        # Deal Cards
        main_dealer.deal_cards()
        
        for i in range(self.num_players):
            print(f"Player {i + 1}: ")
            print(f"Your cards are -> ")
            print(self.cards.print_cards(self.players[i].cards))
        
        bets = betting_logic.BettingLogic(self)
        
        # Place bets (Pre-Flop)
        bets.betting_round(preFlop=True)
        
        # Show first 3 cards on table
        main_dealer.open_table_cards(isPreFlop=True)
        
        bets.betting_round(preFlop=False)
        
        main_dealer.open_table_cards(isPreFlop=False)
        
        bets.betting_round(preFlop=False)
        
        import hand_evaluator
        
        he = hand_evaluator.Evaluator(self)
        
        winner = he.evaluate_hands()
        
        
        
        
    
    def create_players(self):
        import player
        
        # Creating Players
        self.players = []
        for i in range(self.num_players):
            self.players.append(player.Player())
        
        return self.players
    
if __name__ == "__main__":
    print("Running poker game...")
    pg = Poker_Game()
    pg.play()
    print("Done. Game complete.")