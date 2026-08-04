from fastapi import APIRouter
import backend.service.game_service
import backend.schemas.game as schema

router = APIRouter(prefix="/game")

gmservice = backend.service.game_service.GameService()

@router.post("/start")
def start_game(req: schema.CreateGameRequest):
    game_id = gmservice.create_game(request=req)
    return {"message": f"Game started. Game => {gmservice.get_game(game_id)}"}

# Can also return like this!!!
# @router.post("/games", response_model=CreateGameResponse)