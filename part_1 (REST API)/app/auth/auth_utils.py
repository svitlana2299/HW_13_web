from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import SECRET_KEY, ALGORITHM
from .models import User

# Створюємо об'єкт для хешування паролів
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функція для хешування паролів


def hash_password(password: str) -> str:
    return password_context.hash(password)

# Функція для перевірки пароля


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

# Функція для отримання користувача з бази даних за ім'ям


def get_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

# Функція для аутентифікації користувача і створення токену доступу


def authenticate_user(username: str, password: str, db: Session) -> dict:
    # Отримуємо користувача з бази даних
    user = get_user(db, username)
    if not user:
        return None  # Користувача не знайдено
    if not verify_password(password, user.password_hash):
        return None  # Невірний пароль
    user_data = {"sub": username}  # Дані для токену
    expires_delta = timedelta(minutes=15)  # Тривалість токену
    access_token = create_access_token(user_data, expires_delta)
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
