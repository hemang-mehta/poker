class Dealer:
    def __init__(self, game):
        self.game = game

    def deal_cards(self):
        for _ in range(2):
            for p in range(self.game.num_players):
                self.game.players[p].cards.append(self.game.full_deck.popleft())
    
    def open_table_cards(self, isPreFlop=True):
        if isPreFlop:
            for i in range(3):
                self.game.table_cards.append(self.game.full_deck.popleft())
        else:
            self.game.table_cards.append(self.game.full_deck.popleft())
    