from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.auth_utils import get_current_user, update_user, upload_avatar

router = APIRouter()


@router.get("/user/", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    # Маршрут для отримання інформації про поточного користувача
    return current_user


@router.put("/user/update/")
def update_current_user(user: User, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    # Маршрут для оновлення інформації про користувача
    return update_user(db, current_user, user)


@router.post("/user/upload-avatar/")
def upload_user_avatar(file: UploadFile, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    # Маршрут для завантаження аватара користувача
    return upload_avatar(db, current_user, file)
