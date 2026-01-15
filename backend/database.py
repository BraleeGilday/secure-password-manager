from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./spm.db"

# check same thread may need to change for Postgres
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

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