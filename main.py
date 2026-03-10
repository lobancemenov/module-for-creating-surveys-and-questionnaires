from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Survey API", description="Модуль для создания опросов", version="0.1.0")

# ----- Модели Pydantic -----
# Модель для создания опроса (все поля обязательные, кроме description)
class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True

# Модель для обновления опроса (все поля необязательные)
class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

# ----- Имитация базы данных -----
# Ключ — ID опроса, значение — словарь с данными опроса
surveys_db = {}

# ----- Вспомогательные функции (для удобства) -----
def get_survey_or_none(survey_id: int):
    """Возвращает опрос из БД или None, если не найден."""
    return surveys_db.get(survey_id)

# ----- Эндпоинты -----

# 1. GET / — приветствие (как в примере)
@app.get("/")
async def home():
    return {"message": "Это API для управления опросами. Перейдите на /docs для тестирования."}

# 2. GET /surveys — получить список всех опросов
@app.get("/surveys")
async def get_all_surveys():
    return surveys_db

# 3. GET /surveys/{survey_id} — получить конкретный опрос по ID
@app.get("/surveys/{survey_id}")
async def get_survey(survey_id: int):
    survey = get_survey_or_none(survey_id)
    if survey is None:
        return {"error": "Опрос не найден"}
    return survey

# 4. POST /surveys/{survey_id} — создать новый опрос с указанным ID
#    (именно так, как в примере с книгами: ID передаётся в пути)
@app.post("/surveys/{survey_id}")
async def create_survey(survey_id: int, new_survey: SurveyCreate):
    if survey_id in surveys_db:
        return {"error": "Опрос с таким ID уже существует"}
    # Добавляем дату создания и сохраняем
    survey_data = new_survey.dict()
    survey_data["created_at"] = datetime.now().isoformat()  # добавим дату создания
    surveys_db[survey_id] = survey_data
    return surveys_db[survey_id]

# 5. PUT /surveys/{survey_id} — обновить существующий опрос
@app.put("/surveys/{survey_id}")
async def update_survey(survey_id: int, updated_data: SurveyUpdate):
    if survey_id not in surveys_db:
        return {"error": "Опрос не найден"}
    # Обновляем только те поля, которые переданы (не равны None)
    current = surveys_db[survey_id]
    if updated_data.title is not None:
        current["title"] = updated_data.title
    if updated_data.description is not None:
        current["description"] = updated_data.description
    if updated_data.is_active is not None:
        current["is_active"] = updated_data.is_active
    return current

# 6. DELETE /surveys/delete-book (как в примере: параметр в query)
#    Для разнообразия оставим такой же стиль, но можно сделать и через path
@app.delete("/surveys/delete")
async def delete_survey(survey_id: int = Query(..., description="ID опроса для удаления")):
    if survey_id not in surveys_db:
        return {"error": "Опрос не найден"}
    del surveys_db[survey_id]
    return {"message": "Опрос успешно удалён"}