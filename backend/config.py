from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

# based on https://fastapi.tiangolo.com/advanced/settings/


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    TIMEOUT: int = 1
    CRED_ENC_KEY: str = "u36sOQjKvp93KNFIL4ACb3WJT-tV4Lp1qH8-XeWu0ko="
  
    # Postrgresql
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str  # must be db in docker
    POSTGRES_PORT: str
    POSTGRES_ENGINE: str

    # AWS
    RDS_HOST: str | None = None
    RDS_PORT: int | None = None
    RDS_USER: str | None = None
    RDS_PWD: str | None = None

    EC2_USER: str | None = None
    EC2_HOST: str | None = None
    EC2_DIRECTORY: str | None = None
    PEM_PATH: str | None = None

    # model_config = SettingsConfigDict(
    #     env_file=".env" if os.getenv("APP_ENV") != "production" else ".env.prod"
    # )


@lru_cache
def get_settings():
    return Settings()
