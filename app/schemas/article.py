# app/schemas/article.py
# app/schemas/article.py
from __future__ import annotations  # <-- Добавь в самое начало

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from app.schemas.base import BaseSchema


class ArticleBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    format: str = Field("plain_text", description="plain_text, markdown, html")
    published: bool = Field(False)

    @validator("format")
    def validate_format(cls, value):
        if value not in ["plain_text", "markdown", "html"]:
            raise ValueError("Format must be plain_text, markdown, or html")
        return value


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    format: Optional[str]
    published: Optional[bool]


class ArticleVersionOut(BaseSchema):
    id: int
    title: str
    content: str
    format: str
    created_at: str


class ArticleOut(ArticleBase):
    id: int
    author_id: int
    created_at: str
    updated_at: str
    versions: List[ArticleVersionOut] = []
    tags: List['TagOut'] = []  # ← строковая аннотация, безопасна благодаря __future__.annotations

    class Config:
        from_attributes = True


# rebuild будет вызван позже — не здесь