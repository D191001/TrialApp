from datetime import UTC, datetime
from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])
active_connections: Dict[int, Set[WebSocket]] = {}


@router.websocket("/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = set()
    active_connections[room_id].add(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = {
                "id": len(active_connections[room_id]),
                "text": data["text"],
                "sender_id": 1,
                "sent_at": datetime.now(UTC).isoformat(),
            }

            for connection in active_connections[room_id]:
                await connection.send_json(message)
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
