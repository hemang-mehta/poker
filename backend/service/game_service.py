import backend.core.game_manager as manager
from backend.schemas.game import CreateGameRequest

class GameService:
    def __init__(self):
        self.manager = manager.GameManager()
    
    def create_game(self, request: CreateGameRequest):
        gmid = self.manager.create_game(player_name = request.host_name, chips = request.starting_money, max_players = request.max_players)
        return gmid