from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.models import UserModel
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db
import jwt



def is_authenticated(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")  # or your source
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user_id = payload.get("_id")
    user = db.query(UserModel).filter(UserModel.id == user_id).first() if user_id else None
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    return user