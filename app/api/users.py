# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, utils
from app.utils.logger import log

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    Проверяет уникальность username и email.
    """
    log.info("User registration attempt", username=user.username, email=user.email)

    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()

    if db_user:
        log.warning("Registration failed: username or email already exists", user_id=db_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем или email уже существует"
        )

    hashed_password = utils.auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    log.info("User registered successfully", user_id=db_user.id)
    return db_user


@router.post("/login")
def login_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя.
    Возвращает JWT-токен.
    """
    log.info("Login attempt", username=user.username)

    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.auth.verify_password(user.password, db_user.hashed_password):
        log.warning("Login failed: invalid credentials", username=user.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = utils.auth.create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    log.info("User logged in", user_id=db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}