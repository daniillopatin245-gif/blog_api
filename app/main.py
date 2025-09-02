# app/main.py
from fastapi import FastAPI
from app.api import users, articles
from app.utils.logger import log  # ✅ Добавлен импорт

app = FastAPI(title="Blog API", description="Production-ready blog API with advanced features")

# Подключаем роуты
app.include_router(users.router)
app.include_router(articles.router)


@app.on_event("startup")
def startup_event():
    log.info("Application startup")  # ✅ Теперь работает


@app.on_event("shutdown")
def shutdown_event():
    log.info("Application shutdown")


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Blog API! Перейдите на /docs для просмотра документации."}
    from app.database import Base, engine

# Создаём все таблицы при запуске
Base.metadata.create_all(bind=engine)