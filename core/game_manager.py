class GameManager:
    def __init__(self):
        self.game_list = []

    def create_game(self, player_name, chips, max_players):
        import poker.game as game
        
        self.game_list.append(game.Poker_Game())
        return len(self.game_list) - 1
    
    def get_game(self, game_id):
        return self.game_list[game_id]
    
    def end_game(self, game_id):
        self.game_list.pop(game_id)
        return True