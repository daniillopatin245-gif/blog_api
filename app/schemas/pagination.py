# app/schemas/pagination.py
from pydantic import BaseModel
from typing import Generic, TypeVar, List
from app.schemas.base import BaseSchema


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Универсальная схема для пагинации.
    Пример ответа:
    {
      "items": [...],
      "total": 100,
      "page": 2,
      "per_page": 10,
      "total_pages": 10
    }
    """
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int