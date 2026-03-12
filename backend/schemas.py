from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True

class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class SurveyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)