# app/schemas/user.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: str = Field(..., description="Email пользователя")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Пароль (минимум 6 символов)")

    @validator("username")
    def validate_username(cls, value):
        # Простая проверка на мат (можно расширить)
        bad_words = ["идиот", "дурак", "бля", "сука"]  # Пример — лучше вынести в файл
        if any(word in value.lower() for word in bad_words):
            raise ValueError("Имя пользователя содержит недопустимые слова")
        return value


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6)

    @validator("password")
    def validate_password(cls, value):
        if value and len(value) < 6:
            raise ValueError("Пароль должен быть не менее 6 символов")
        return value


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: Optional[str] = None  # ✅ str, не datetime

    class Config:
        from_attributes = True