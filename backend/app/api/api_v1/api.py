from app.api.api_v1.endpoints import (
    auth,
    likes,
    messages,
    profile,
    rooms,
    search,
    ws,
)
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router.include_router(
    messages.router, prefix="/messages", tags=["messages"]
)
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])
