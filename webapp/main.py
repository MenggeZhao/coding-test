#!/usr/bin/env python3

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # list of keeping track of active WebSocket connections
        self.active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, username: str):
        """
        Accepts a new WebSocket connection and adds it to the active connections list.
        """
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "username": username})        
        # tell all users that a new user has joined
        await self.broadcast(f"{username} has joined the chat.")
        


    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        for conn in self.active_connections:
            if conn["websocket"] == websocket:
                username = conn["username"]
                self.active_connections.remove(conn)
                return username
        return None          

    async def broadcast(self, message: str):
        """
        Send a message to all connected clients.
        """
        disconnected_clients = []
        
        for conn in self.active_connections:
            try:
                await conn["websocket"].send_text(message)
            except WebSocketDisconnect:
                disconnected_clients.append(conn)

        # Remove any clients that failed to receive messages
        for conn in disconnected_clients:
            self.active_connections.remove(conn)

            
# create an instance of the ConnectionManager to manage WebSocket connections
manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """
    Handles WebSocket connections for users.
    """
    await manager.connect(websocket, username)
    try:
        while True:
            # receive a message from the client
            message = await websocket.receive_text()
            # broadcast username and its message
            broadcast_message = f"{username}: {message}"
            await manager.broadcast(broadcast_message)
            
    except WebSocketDisconnect:
        # disconnect a client and tell others
        disconnected_user = manager.disconnect(websocket)
        if disconnected_user:
            await manager.broadcast(f"{disconnected_user} has left the chat.")
            

