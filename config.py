# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pass

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()