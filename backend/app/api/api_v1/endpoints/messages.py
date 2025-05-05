from datetime import UTC, datetime
from typing import Dict

from app.core.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str


router = APIRouter()


# Изменяем пути, убираем '/messages' из начала пути
@router.post("/{room_id}/messages")
async def send_message(
    room_id: int,
    message: MessageCreate,
    current_user=Depends(get_current_user),
) -> Dict:
    return {
        "id": 1,
        "text": message.text,
        "sender_id": 1,
        "sent_at": datetime.now(UTC).isoformat(),
    }


@router.get("/{room_id}/messages")
async def get_messages(room_id: int, current_user=Depends(get_current_user)):
    return [
        {
            "id": 1,
            "text": "Привет всем!",
            "sender_id": 1,
            "sent_at": "2023-10-01T12:00:00Z",
        }
    ]
