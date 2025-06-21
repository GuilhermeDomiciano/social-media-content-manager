# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    PROJECT_NAME: str = "Social Media Content Manager Backend"
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Adicione esta linha!

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()