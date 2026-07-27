class Cards:
    def __init__(self):
        self.card_classes = [
            1,  # Spade
            2,  # Diamond
            3,  # Club
            4   # Heart
        ]
        
        self.cards = [i for i in range(1, 14)] # 12,13,14 -> (Jack, Queen, King)
        
        self.full_deck = [f"{i}_{j}" for i in self.card_classes for j in self.cards]
    
    def get_full_deck(self):
        return self.full_deck
    
    def shuffle_cards(self, cards):
        import random
        
        random.shuffle(cards)

if __name__ == "__main__":
    import main
    main.run()