from fastapi import WebSocket
from typing import Dict, Set
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, person_id: str):
        await websocket.accept()
        if person_id not in self.active_connections:
            self.active_connections[person_id] = set()
        self.active_connections[person_id].add(websocket)

    def disconnect(self, websocket: WebSocket, person_id: str):
        if person_id in self.active_connections:
            self.active_connections[person_id].discard(websocket)
            if not self.active_connections[person_id]:
                del self.active_connections[person_id]

    async def broadcast_to_person(self, person_id: str, message: dict):
        if person_id in self.active_connections:
            dead_connections = set()
            for websocket in self.active_connections[person_id]:
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    dead_connections.add(websocket)
            self.active_connections[person_id] -= dead_connections

