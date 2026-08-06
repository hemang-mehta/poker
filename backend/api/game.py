from fastapi import APIRouter
import service.game_service
import schemas.game as schema
from schemas.game import CreateGameRequest

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