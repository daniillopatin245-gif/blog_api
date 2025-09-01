# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# --- Добавляем путь к корню проекта ---
# Получаем путь к папке, где лежит migrations (т.е. корень проекта)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Добавляем корень проекта в sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Теперь можно импортировать app
try:
    from app.database import Base, engine
    from app.models import user, article, tag, article_version  # Импортируем модели для отслеживания
except ModuleNotFoundError as e:
    raise ImportError(f"Не удалось импортировать модуль: {e}. Убедитесь, что app/ — это пакет и путь добавлен.") from e

# Конфигурация Alembic
config = context.config

# Настройка логирования из .ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для генерации миграций
target_metadata = Base.metadata

# Функция для онлайн-миграций
def run_migrations_online():
    # Используем engine из app.database
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Отслеживать изменения типов (например, VARCHAR(50) → VARCHAR(100))
            render_as_batch=True  # Полезно при работе с SQLite, но не мешает в PostgreSQL
        )

        with context.begin_transaction():
            context.run_migrations()

# Запускаем миграции
run_migrations_online()