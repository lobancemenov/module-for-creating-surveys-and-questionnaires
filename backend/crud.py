from sqlalchemy.orm import Session
from typing import List, Optional
from models import SurveyModel
from schemas import SurveyCreate, SurveyUpdate


# ===== CREATE =====
def create_survey(db: Session, survey: SurveyCreate) -> SurveyModel:
    survey_data = SurveyModel(**survey.model_dump())
    db.add(survey_data)
    db.commit()
    db.refresh(survey_data)
    return survey_data


# ===== READ (все) =====
def get_all_surveys(db: Session) -> List[SurveyModel]:
    return db.query(SurveyModel).all()


# ===== READ (один по ID) =====
def get_survey(db: Session, survey_id: int) -> Optional[SurveyModel]:
    return db.query(SurveyModel).filter(SurveyModel.id == survey_id).first()


# ===== READ (поиск по атрибутам) =====
def search_surveys(
        db: Session,
        title: Optional[str] = None,
        is_active: Optional[bool] = None
) -> List[SurveyModel]:
    query = db.query(SurveyModel)
    if title:
        query = query.filter(SurveyModel.title.contains(title))
    if is_active is not None:
        query = query.filter(SurveyModel.is_active == is_active)
    return query.all()


# ===== UPDATE =====
def update_survey(
        db: Session,
        survey_id: int,
        survey_data: SurveyUpdate
) -> Optional[SurveyModel]:
    survey = get_survey(db, survey_id)
    if survey is None:
        return None

    if survey_data.title is not None:
        survey.title = survey_data.title
    if survey_data.description is not None:
        survey.description = survey_data.description
    if survey_data.is_active is not None:
        survey.is_active = survey_data.is_active

    db.commit()
    db.refresh(survey)
    return survey


# ===== DELETE =====
def delete_survey(db: Session, survey_id: int) -> bool:
    survey = get_survey(db, survey_id)
    if survey is None:
        return False

    db.delete(survey)
    db.commit()
    return True