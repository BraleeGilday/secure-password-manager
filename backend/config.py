from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache
import os

# based on https://fastapi.tiangolo.com/advanced/settings/


class Settings(BaseSettings):
    # refactored database.py with help from gemini
    APP_ENV: str = os.getenv("APP_ENV", "development")

    # JWT
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    TIMEOUT: int = 1
    CRED_ENC_KEY: str = "u36sOQjKvp93KNFIL4ACb3WJT-tV4Lp1qH8-XeWu0ko="
  
    # Postrgresql
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "default"
    POSTGRES_DB: str = "spm_db"
    POSTGRES_HOST: str = "localhost"  # must be db in docker
    POSTGRES_PORT: str = "5432"
    POSTGRES_ENGINE: str = "postgresql+psycopg2"

    # AWS
    RDS_HOST: str | None = None
    RDS_PORT: int | None = None
    RDS_USER: str | None = None
    RDS_PWD: str | None = None

    EC2_USER: str | None = None
    EC2_HOST: str | None = None
    EC2_DIRECTORY: str | None = None
    PEM_PATH: str | None = None

    @computed_field
    @property
    def create_database_url(self) -> str:
        dev_env = self.APP_ENV == "development"
        ENGINE = self.POSTGRES_ENGINE
        USER = self.POSTGRES_USER if dev_env else self.RDS_USER
        PWD = self.POSTGRES_PASSWORD if dev_env else self.RDS_PWD
        HOST = self.POSTGRES_HOST if dev_env else self.RDS_HOST
        PORT = self.POSTGRES_PORT if dev_env else self.RDS_PORT
        DB = self.POSTGRES_DB
        
        return f"{ENGINE}://{USER}:{PWD}@{HOST}:{PORT}/{DB}"

    @property
    def connect_args(self) -> dict:
        dev_env = self.APP_ENV == "development"
        return {"sslmode": "require"} if not dev_env else {}
    
    # model_config = SettingsConfigDict(
    #     env_file=".env" if os.getenv("APP_ENV") != "production" else ".env.prod"
    # )


@lru_cache
def get_settings():
    return Settings()
