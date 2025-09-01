try:
    from app.database import Base
    from app.models import user, article, tag, article_version
    print("✅ Все модули импортированы успешно!")
    print("Tables:", Base.metadata.tables.keys())
except Exception as e:
    print("❌ Ошибка:", e)