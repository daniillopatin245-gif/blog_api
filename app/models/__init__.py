# app/models/__init__.py
# Импортируем модели, чтобы их можно было использовать как:
# from app.models import User, Article, Tag

from .user import User
from .article import Article
from .tag import Tag
from .article_version import ArticleVersion

# Опционально: экспорт всех
__all__ = ["User", "Article", "Tag", "ArticleVersion"]