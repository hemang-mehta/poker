from pydantic import BaseModel, Field
from typing import List, Optional

class CreateGameRequest(BaseModel):
    host_name: str = Field(min_length=1, max_length=30)
    starting_money: int = Field(gt=0)
    max_players: int = Field(ge=2, le=9)

class CreateGameResponse(BaseModel):
    game_id: str
    message: str = "Game created successfully!"

class PlayerResponse(BaseModel):
    player_id: int
    player_name: str
    curr_money_left: int
    is_bot: bool
    all_in: bool
    fold: bool
    eliminated: bool
    curr_round_bet: int

class PlayerWithCardsResponse(PlayerResponse):
    cards: List[str]

class GameResponse(BaseModel):
    guid: str
    small_blind: int
    big_blind: int
    max_players: int
    num_players: int
    pot: int
    table_cards: List[str]
    players: List[PlayerResponse]

class PlayerAction(BaseModel):
    type: str
    action: str
    amount: int
    gameid: str
    player_id: int