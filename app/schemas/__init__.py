# app/schemas/__init__.py
from .user import UserBase, UserCreate, UserUpdate, UserOut
from .article import ArticleBase, ArticleCreate, ArticleUpdate, ArticleOut, ArticleVersionOut
from .tag import TagBase, TagCreate, TagUpdate, TagOut
from .pagination import PaginatedResponse

# Разрешаем циклические ссылки
ArticleOut.model_rebuild()
TagOut.model_rebuild()

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserOut",
    "ArticleBase", "ArticleCreate", "ArticleUpdate", "ArticleOut", "ArticleVersionOut",
    "TagBase", "TagCreate", "TagUpdate", "TagOut",
    "PaginatedResponse",
]