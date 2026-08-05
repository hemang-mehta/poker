from pydantic import BaseModel, Field

class CreateGameRequest(BaseModel):
    host_name: str = Field(min_length=1, max_length=30)
    starting_money: int = Field(gt=0)
    max_players: int = Field(ge=2, le=9)

# class CreateGameResponse(BaseModel):
#     game_id: int