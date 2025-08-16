from typing import Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections:Dict[str,WebSocket]={}

    async def connect(self, student_id: str,websocket:WebSocket):
        await websocket.accept()
        self.active_connections[student_id] =websocket

    def disconnect(self,student_id:str):
        self.active_connections[student_id] = WebSocket

    async def send_to_user(self,student_id:str,message:dict):
        ws = self.active_connections.get(student_id)
        if ws:
            await ws.send_json(message)

ws_manager = WebSocketManager()

    