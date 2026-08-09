from poker.game import PokerGame

class Dealer:
    def __init__(self, game):
        self.game: PokerGame = game

    def deal_cards(self):
        for _ in range(2):
            for p in range(self.game.num_players):
                self.game.players[p].cards.append(self.game.full_deck.popleft())
    
    """Removes one card from the top of the shuffled deck"""
    def open_table_card(self):
        self.game.table_cards.append(self.game.full_deck.popleft())
    