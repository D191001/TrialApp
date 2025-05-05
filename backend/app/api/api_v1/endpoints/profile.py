from app.api.api_v1.endpoints.auth import get_current_user_from_jwt
from app.core.security import get_current_user
from app.schemas.user import UserInDB, UserUpdate
from fastapi import APIRouter, Depends, File, UploadFile, status

router = APIRouter()


@router.get("")
async def get_profile(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@router.put("")
async def update_profile(
    update_data: UserUpdate, current_user: UserInDB = Depends(get_current_user)
):
    return {"message": "Профиль успешно обновлен"}


@router.post("/photos")
async def upload_photo(
    photo: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user),
):
    return {
        "message": "Фотография успешно загружена",
        "photo_url": f"https://example.com/uploads/{photo.filename}",
    }


@router.get("/secure")
async def secure_profile(current_user=Depends(get_current_user_from_jwt)):
    return {"message": "Доступ разрешён", "user": current_user}
