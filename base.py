# app/schemas/base.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any

class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()  # datetime -> ISO строка: "2025-09-02T10:40:54.370130"
        }
    }