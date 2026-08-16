from schemas.game import CreateGameRequest

class GameManager:    
    def __init__(self):
        self.game_data = {}

    async def create_game(self, request: CreateGameRequest):
        import poker.game as game
        import uuid
        import asyncio

        my_guid = uuid.uuid4()
        guid_str = str(my_guid)

        p_game = game.PokerGame(guid = guid_str, **request.model_dump(exclude_none=True))
        self.game_data[guid_str] = p_game

        # Start the game loop in the background
        asyncio.create_task(p_game.action())

        return guid_str
    
    def get_game(self, guid):
        return self.game_data[guid]
    
    def end_game(self, guid):
        self.game_data.pop(guid)
        return True