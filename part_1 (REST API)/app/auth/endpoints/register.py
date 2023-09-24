from app.email.sendgrid import send_verification_email  # Додайте імпорт
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.auth_utils import create_user

router = APIRouter()


@router.post("/register/", response_model=User)
def register_user(user: User, db: Session = Depends(SessionLocal)):
    # Маршрут для реєстрації нового користувача
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return create_user(db, user)
