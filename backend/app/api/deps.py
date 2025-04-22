from app.core import security
from app.db.database import get_db
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


async def get_current_user(
    session: str = Cookie(default=None), db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = security.verify_token(session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user
