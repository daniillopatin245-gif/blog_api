from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Базовая схема, от которой наследуются все остальные.
    Можно добавить общие поля или методы в будущем.
    """
    class Config:
        from_attributes = True  # Ранее было orm_mode=True (для Pydantic v2)