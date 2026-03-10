from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# ===== Для создания опроса =====
class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


# ===== Для обновления опроса =====
class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# ===== Для ответа API =====
class SurveyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)