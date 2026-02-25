from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.environ["POSTGRES_USER"]
PWD = os.environ.get("POSTGRES_PASSWORD", "default")
DB = os.environ.get("POSTGRES_DB", "spm_db")
HOST = os.environ.get("POSTGRES_HOST", "localhost")
PORT = os.environ.get("POSTGRES_PORT", "5432")
ENGINE = os.environ.get("POSTGRES_ENGINE", "postgresql+psycopg2")

SQLALCHEMY_DATABASE_URL = "sqlite:///./spm.db"
POSTGRES_DB_URL = (
    f"{ENGINE}://{USER}:{PWD}@{HOST}:{PORT}/{DB}"
)

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
