from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()
POSTGRES_DB_URL = settings.create_database_url
# SQLALCHEMY_DATABASE_URL = "sqlite:///./spm.db"

engine = create_engine(POSTGRES_DB_URL, connect_args=settings.connect_args)

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
