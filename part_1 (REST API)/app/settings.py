from pydantic import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_file = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    CORS_ORIGINS: list = ["*"]  # Домени, з яких дозволені запити


settings = Settings()
