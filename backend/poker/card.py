class Cards:
    def __init__(self):
        self.card_classes = [
            1,  # Spade
            2,  # Diamond
            3,  # Club
            4   # Heart
        ]
        
        self.cards = [i for i in range(1, 14)] # 11,12,13 -> (Jack, Queen, King)
    
    def print_cards(self, cards_list):
        card_names = []
        for i in cards_list:
            card_name = ''
            if i.split('_')[0] == '1': card_name += 'Spade'
            elif i.split('_')[0] == '2': card_name += 'Diamond'
            elif i.split('_')[0] == '3': card_name += 'Club'
            elif i.split('_')[0] == '4': card_name += 'Heart'

            card_name += f" {i.split('_')[-1]}"
            card_names.append(card_name)
        return card_names

if __name__ == "__main__":
    import backend.poker.game as game
    game.run()