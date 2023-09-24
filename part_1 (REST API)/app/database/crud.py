# database/crud.py
from sqlalchemy.orm import Session
from .models import User
from fastapi import HTTPException, Depends, status
from app.auth.jwt import verify_password, create_access_token, get_current_user


def create_user(db: Session, user: User):
    """
    Створення нового користувача.
    """
    db_user = User(**user.dict())
    db_user.password = HashPassword.get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    """
    Отримання користувача за іменем користувача.
    """
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    """
    Аутентифікація користувача та створення JWT токену.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not HashPassword.verify_password(password, user.password):
        return None
    access_token = create_access_token(data={"sub": user.username})
    return access_token


def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Перевірка активного користувача.
    """
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")
