from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
from schemas import SurveyCreate, SurveyUpdate, SurveyResponse
import crud

# ===== Роутер =====
router = APIRouter(prefix="/surveys", tags=["Опросы"])

# ===== GET /surveys — все опросы =====
@router.get("", response_model=List[SurveyResponse])
async def get_all_surveys(db: Session = Depends(get_db)):
    return crud.get_all_surveys(db)

# ===== GET /surveys/{survey_id} — один опрос =====
@router.get("/{survey_id}", response_model=SurveyResponse)
async def get_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = crud.get_survey(db, survey_id)
    if survey is None:
        raise HTTPException(status_code=404, detail="Опрос не найден")
    return survey

# ===== GET /surveys/search — поиск =====
@router.get("/search", response_model=List[SurveyResponse])
async def search_surveys(
    title: Optional[str] = Query(None, description="Поиск по названию"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    db: Session = Depends(get_db)
):
    return crud.search_surveys(db, title, is_active)

# ===== POST /surveys — создать опрос =====
@router.post("", response_model=SurveyResponse)
async def create_survey(survey: SurveyCreate, db: Session = Depends(get_db)):
    return crud.create_survey(db, survey)

# ===== PUT /surveys/{survey_id} — обновить опрос =====
@router.put("/{survey_id}", response_model=SurveyResponse)
async def update_survey(
    survey_id: int,
    survey_data: SurveyUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_survey(db, survey_id, survey_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Опрос не найден")
    return updated

# ===== DELETE /surveys/{survey_id} — удалить опрос =====
@router.delete("/{survey_id}")
async def delete_survey(survey_id: int, db: Session = Depends(get_db)):
    success = crud.delete_survey(db, survey_id)
    if not success:
        raise HTTPException(status_code=404, detail="Опрос не найден")
    return {"message": "Опрос успешно удалён"}