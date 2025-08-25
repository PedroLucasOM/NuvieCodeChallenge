from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost/nuvie_db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    synthea_base_url: str = "https://synthea.mitre.org/"
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    environment: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
