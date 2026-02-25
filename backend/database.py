from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


ENV = os.getenv("APP_ENV", "development")
if ENV == "development":
    load_dotenv(".env")
else:
    load_dotenv(".env.prod")

if ENV == "development":
    USER = os.environ["POSTGRES_USER"]
    PWD = os.environ.get("POSTGRES_PASSWORD", "default")
    HOST = os.environ.get("POSTGRES_HOST", "localhost")
    PORT = os.environ.get("POSTGRES_PORT", "5432")
    DB = os.environ.get("POSTGRES_DB", "spm_db")
    ENGINE = os.environ.get("POSTGRES_ENGINE", "postgresql+psycopg2")

    connect_args = {}

else:
    USER = os.environ["RDS_USER"]
    PWD = os.environ.get("RDS_PWD")
    HOST = os.environ.get("RDS_HOST")
    PORT = os.environ.get("RDS_PORT", "5432")
    DB = os.environ.get("POSTGRES_DB")
    ENGINE = os.environ.get("POSTGRES_ENGINE", "postgresql+psycopg2")

    connect_args = {"sslmode": "require"}

SQLALCHEMY_DATABASE_URL = "sqlite:///./spm.db"
POSTGRES_DB_URL = (
    f"{ENGINE}://{USER}:{PWD}@{HOST}:{PORT}/{DB}"
)

engine = create_engine(POSTGRES_DB_URL, connect_args=connect_args)

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
