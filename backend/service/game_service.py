import core.game_manager as manager
from schemas.game import CreateGameRequest

class GameService:
    def __init__(self):
        self.manager = manager.GameManager()
    
    async def create_game(self, request: CreateGameRequest):
        gmid = await self.manager.create_game(request = request)
        return gmid
    
    def get_game(self, gameid: str):
        game_obj = self.manager.get_game(gameid)
        return game_obj