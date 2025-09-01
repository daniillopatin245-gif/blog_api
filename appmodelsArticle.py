# app/models/article.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class ContentFormat(str, enum.Enum):
    plain_text = "plain_text"
    markdown = "markdown"
    html = "html"

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    format = Column(Enum(ContentFormat), default=ContentFormat.plain_text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = Column(Boolean, default=False)

    # Связи
    author = relationship("User", back_populates="articles")
    versions = relationship("ArticleVersion", back_populates="article", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")