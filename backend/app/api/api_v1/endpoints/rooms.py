from typing import Dict

from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    description: str
    is_private: bool = False


router = APIRouter()


@router.post("")
async def create_room(
    room: RoomCreate, current_user=Depends(get_current_user)
) -> Dict:
    return {
        "id": 1,
        "name": room.name,
        "description": room.description,
        "is_private": room.is_private,
        "owner_id": 1,
    }


@router.get("/{room_id}")
async def get_room(room_id: int, current_user=Depends(get_current_user)):
    return {
        "id": room_id,
        "name": "Название комнаты",
        "description": "Описание комнаты",
        "is_private": False,
        "participants": [
            {"id": 1, "name": "Владелец комнаты"},
            {"id": 2, "name": "Участник комнаты"},
        ],
    }


class InviteUser(BaseModel):
    user_id: int


@router.post("/{room_id}/invite")
async def invite_to_room(
    room_id: int, invite: InviteUser, current_user=Depends(get_current_user)
):
    return {"message": "Пользователь приглашен"}
