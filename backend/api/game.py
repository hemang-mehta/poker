from typing import Optional
from fastapi import APIRouter, WebSocket, Query
import service.game_service
import schemas.game as schema
from schemas.game import CreateGameRequest, GameResponse, CreateGameResponse, PlayerAction, PlayerWithCardsResponse, PlayerResponse
from core.connection_manager import manager as connection_manager
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from poker.game import PokerGame

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

gmservice = service.game_service.GameService()

@router.post("/start")
def start_game(req: CreateGameRequest):
    return {"message": "Starting game..."}

@router.post("/creategame", response_model=CreateGameResponse)
def create_game(req: CreateGameRequest):
    guid = gmservice.create_game(request=req)
    return CreateGameResponse(
        game_id=guid
    )

@router.get("/{gameid}")
def get_game(gameid: str, player_id: Optional[int] = Query(None)):
    game = gmservice.get_game(gameid)

    # Filter players based on the player_id requesting the data
    filtered_players = []
    for p in game.players:
        if player_id is not None and p.player_id == player_id:
            # This is the requesting player, show their cards
            filtered_players.append(PlayerWithCardsResponse(**p.__dict__))
        else:
            # Other players, hide their cards
            filtered_players.append(PlayerResponse(**p.__dict__))

    # Construct the response manually since the players list is now mixed types
    return {
        "guid": game.guid,
        "small_blind": game.small_blind,
        "big_blind": game.big_blind,
        "max_players": game.max_players,
        "num_players": game.num_players,
        "pot": game.pot,
        "table_cards": game.table_cards,
        "players": filtered_players,
        "state": game.state
    }

@router.websocket("/game_data")
async def get_curr_game_data(websocket: WebSocket, game_id: str = Query(...)):
    await connection_manager.connect(game_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            req_obj: PlayerAction = json.loads(data)
            game: PokerGame = gmservice.get_game(req_obj.gameid)
            game.handle_player_action(player_id=req_obj.player_id, action_type=req_obj.action, amount=req_obj.amount)
    except Exception as e:
        print(e)
    finally:
        connection_manager.disconnect(game_id, websocket)
