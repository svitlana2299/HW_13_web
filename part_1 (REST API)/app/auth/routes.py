from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.models import UserDB, UserPydantic
from app.auth.jwt import create_access_token, verify_token, TokenData
from app.auth.auth_utils import hash_password, verify_password
from app.email import send_email
from app.database import get_db

router = APIRouter()


@router.post("/register/", response_model=UserPydantic)
def register_user(user: UserDB, db: Session = Depends(get_db)):
    # Реєстрація нового користувача
    user_exists = db.query(UserDB).filter(UserDB.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already registered")
    user.password_hash = hash_password(user.password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login/", response_model=dict)
def login_user(user_data: dict, db: Session = Depends(get_db)):
    # Вхід користувача і отримання токенів
    user = db.query(UserDB).filter(UserDB.email == user_data["email"]).first()
    if user is None or not verify_password(user_data["password"], user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email/")
def verify_email(token: str):
    # Верифікація електронної пошти користувача за токеном
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user_email = payload.get("sub")
    # Додаткова логіка для верифікації пошти, наприклад, позначення користувача як верифікованого
    return {"message": "Email verified successfully"}
