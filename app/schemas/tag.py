# app/schemas/tag.py
from __future__ import annotations  # <-- Добавь в начало

from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.base import BaseSchema


class TagBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagOut(TagBase):
    id: int
    usage_count: int
    created_at: Optional[str] = None
    articles: List['ArticleOut'] = []  # ← можно и так, если нужно

    class Config:
        from_attributes = True


# rebuild будет вызван позже