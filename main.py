class Poker_Game:
    
    def __init__(self):
        import cards
        self.c = cards.Cards()
        
        # Full Deck
        self.full_deck = self.c.get_full_deck()
        self.num_players = 3
        self.players = []
    
    def play(self):
        # Shuffle Deck
        self.c.shuffle_cards(self.full_deck)
        
        # Get Players
        self.create_players()
        print(self.players)
        
        # Deal Cards
        self.deal_cards()
            
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