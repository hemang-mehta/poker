import random
import poker.card as card
# from collections import deque

class Deck:
    def __init__(self):
        self.full_deck = []
        self.cards = card.Cards()
    
    def create_full_deck(self):
        self.full_deck = [f"{i}_{j}" for i in self.cards.card_classes for j in self.cards.cards]
        self.shuffle_cards(self.full_deck)
        # self.full_deck = deque(self.full_deck)
    
    def shuffle_cards(self, cards):
        random.shuffle(cards)