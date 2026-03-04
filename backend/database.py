import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# Prefer Postgres when configured (Docker/prod)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fall back to whatever config.py builds (likely Postgres)
    DATABASE_URL = getattr(settings, "create_database_url", None)

# If it's Postgres but server isn't running locally, allow explicit override:
USE_SQLITE = os.getenv("USE_SQLITE", "0") == "1"

if USE_SQLITE:
    engine = create_engine(
        "sqlite:///./spm.db",
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL, connect_args=settings.connect_args)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()