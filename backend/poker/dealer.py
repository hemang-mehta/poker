from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from poker.game import PokerGame

class Dealer:
    def __init__(self, game):
        self.game: PokerGame = game

    def deal_cards(self):
        for _ in range(2):
            for p in range(self.game.max_players):
                self.game.players[p].cards.append(self.game.full_deck.pop())
    
    """Removes one card from the top of the shuffled deck"""
    def open_table_card(self):
        self.game.table_cards.append(self.game.full_deck.pop())
    