from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.database import Base
from sqlalchemy import Column, Integer, String


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


UserPydantic = sqlalchemy_to_pydantic(UserDB)
