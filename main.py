class Poker_Game:
    
    def __init__(self):
        import cards
        
        self.cards = cards.Cards()
        
        # Full Deck
        self.full_deck = self.cards.get_full_deck()
        self.num_players = 3
        self.players = []
        self.pot = 0
        self.small_blind = 100
        self.big_blind = 200
    
    def play(self):
        import betting_logic
        
        # Shuffle Deck
        self.cards.shuffle_cards(self.full_deck)
        
        # Get Players
        self.create_players()
        
        # Deal Cards
        self.deal_cards()
        
        for i in range(self.num_players):
            print(f"Player {i + 1}: ")
            print(f"Your cards are -> ")
            print(self.cards.print_cards(self.players[i].cards))
        
        bets = betting_logic.BettingLogic(self)
        
        bets.betting_round(preFlop=True)
        
        
    
    def create_players(self):
        import player
        
        # Creating Players
        self.players = []
        for i in range(self.num_players):
            self.players.append(player.Player())
        
        return self.players
    
    def deal_cards(self):
        for p in range(self.num_players):
            self.players[p].cards.append(self.full_deck[p])
            self.players[p].cards.append(self.full_deck[p + self.num_players])

    
if __name__ == "__main__":
    print("Running poker game...")
    pg = Poker_Game()
    pg.play()
    print("Done. Game complete.")