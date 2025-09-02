# app/config.py

class Settings:
    database_url: str = "sqlite:///./blog.db"
    secret_key: str = "your-super-secret-jwt-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"

settings = Settings()