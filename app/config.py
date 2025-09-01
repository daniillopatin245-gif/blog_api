# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str
    debug: bool

    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    celery_broker_url: str
    celery_result_backend: str

    log_level: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Экземпляр настроек
settings = Settings()