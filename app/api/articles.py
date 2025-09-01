from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app import models, schemas, utils
from app.utils.logger import log
from app.utils.auth import decode_access_token
from app.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/articles", tags=["Articles"])


def get_current_user(token: str = Depends(utils.auth.oauth2_scheme), db: Session = Depends(get_db)):
    """
    Получение текущего пользователя по токену.
    Используется как зависимость в защищённых маршрутах.
    """
    payload = decode_access_token(token)
    if not payload:
        log.warning("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учётные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учётные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


@router.post("/", response_model=schemas.ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Создание новой статьи.
    Автоматически сохраняется как первая версия.
    """
    log.info("Article creation", user_id=current_user.id, title=article.title)

    db_article = models.Article(
        title=article.title,
        content=article.content,
        format=article.format,
        author_id=current_user.id,
        published=article.published
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    # Сохраняем как первую версию
    version = models.ArticleVersion(
        article_id=db_article.id,
        title=article.title,
        content=article.content,
        format=article.format
    )
    db.add(version)
    db.commit()

    log.info("Article created", article_id=db_article.id)
    return db_article


@router.get("/", response_model=PaginatedResponse[schemas.ArticleOut])
def list_articles(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    published: Optional[bool] = None,
    tag: Optional[List[str]] = Query(None),
    sort: str = Query("-created_at"),
):
    """
    Получение списка статей с пагинацией, фильтрацией и сортировкой.
    Поддерживает фильтрацию по тегам и статусу публикации.
    """
    query = db.query(models.Article)

    if published is not None:
        query = query.filter(models.Article.published == published)

    if tag:
        query = query.join(models.Article.tags).filter(models.Tag.name.in_(tag))

    # Сортировка
    if sort == "created_at":
        query = query.order_by(models.Article.created_at.asc())
    elif sort == "-created_at":
        query = query.order_by(models.Article.created_at.desc())
    else:
        query = query.order_by(models.Article.created_at.desc())  # По умолчанию

    total = query.count()
    articles = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse(
        items=articles,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total - 1) // per_page + 1
    )


@router.get("/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    Получение статьи по ID.
    Возвращает также историю версий и теги.
    """
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        log.warning("Article not found", article_id=article_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Статья не найдена")
    return article