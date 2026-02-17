from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_DB = os.environ.get("POSTGRES_DB", POSTGRES_USER)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
POSTGRES_ENGINE = os.environ.get("POSTGRES_ENGINE", "postgresql+psycopg2")

SQLALCHEMY_DATABASE_URL = "sqlite:///./spm.db"
POSTGRES_DB_URL = f"{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/spm_db"

engine = create_engine(POSTGRES_DB_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    access db with generator
    """
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
