from fastapi import APIRouter, WebSocket, Query
import service.game_service
import schemas.game as schema
from schemas.game import CreateGameRequest
from core.connection_manager import manager as connection_manager

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

gmservice = service.game_service.GameService()

@router.post("/start")
def start_game(req: CreateGameRequest):
    # game_id = gmservice.create_game(request=req)
    # return {"message": f"Game started. Game => {gmservice.get_game(game_id)}"}
    return {"message": "Starting game..."}

@router.post("/creategame")
def create_game(req: CreateGameRequest):
    guid = gmservice.create_game(request=req)
    return guid

@router.get("/{gameid}")
def get_game(gameid):
    return gmservice.get_game(gameid)

@router.websocket("/game_data")
async def get_curr_game_data(websocket: WebSocket, game_id: str = Query(...)):
    await connection_manager.connect(game_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any messages from client if necessary
    except Exception:
        pass
    finally:
        connection_manager.disconnect(game_id, websocket)
