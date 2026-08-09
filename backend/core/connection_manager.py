from fastapi import WebSocket
from typing import Dict, Set

class ConnectionManager:
    def __init__(self):
        # Maps game_id -> set of active WebSockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, game_id: str, websocket: WebSocket):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = set()
        self.active_connections[game_id].add(websocket)

    def disconnect(self, game_id: str, websocket: WebSocket):
        if game_id in self.active_connections:
            try:
                self.active_connections[game_id].remove(websocket)
                if not self.active_connections[game_id]:
                    del self.active_connections[game_id]
            except KeyError:
                pass

    async def broadcast_to_game(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            for connection in list(self.active_connections[game_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    # Handle disconnected clients that weren't explicitly removed
                    self.disconnect(game_id, connection)

# Singleton instance
manager = ConnectionManager()
