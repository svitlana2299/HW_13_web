from fastapi import FastAPI
from app.api.api_v1.api import router as api_router
from app.core.config import settings
from app.db import init_db
from app.core.middleware import db_session_middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(db_session_middleware, db_url=settings.DATABASE_URL)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Додаємо CORS (Cross-Origin Resource Sharing) для дозволу запитів з вказаних доменів
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    init_db(app)
