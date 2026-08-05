import core.game_manager as manager
from schemas.game import CreateGameRequest

class GameService:
    def __init__(self):
        self.manager = manager.GameManager()
    
    def create_game(self, request: CreateGameRequest):
        gmid = self.manager.create_game(request = request)
        return gmid