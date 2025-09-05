# Блог API — Готовый к продакшену REST API

Полноценный API для блога на **FastAPI**, с поддержкой JWT, черновиков, тегов и валидации.  

---

## Возможности

- ✅ **Аутентификация через JWT** — регистрация и вход
- ✅ **Поддержка форматов** — `plain_text`, `markdown`, `html`
- ✅ **Черновики и история версий** — как в WordPress
- ✅ **Система тегов** — с подсчётом популярности
- ✅ **Умная валидация**:
  - Запрет матерных слов в логинах
  - Проверка на дубли заголовков
- ✅ **Пагинация, фильтрация, сортировка**:
  - Пример: `GET /articles?tag=python&sort=-created_at`
- ✅ **Структурированное логирование** (structlog)
- ✅ **Кастомные ошибки API**:
  json
  {
    "error": {
      "code": "article_not_found",
      "message": "Статья с таким ID не найдена."
    }
  }
		
- ✅ Конфигурация через .env
- ✅ Тесты и чистая история коммитов

 Как запустить
### 1. Клонируй репозиторий
git clone https://github.com/ТВОЙ_НИК/blog_api.git
cd blog_api
### 2. Создай виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows или source venv/bin/activate  # Linux/Mac
### 3. Установи зависимости
pip install -r requirements.txt
### 4. Настрой переменные окружения
copy .env.example .env  # Windows или cp .env.example .env  # Linux/Mac
### 5. Запусти сервер
uvicorn app.main:app --reload

Открой документацию: http://localhost:8000/docs