from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.answer import CheckinAnswerCreate
from app.services.crud_answer import create_answer
from app.database import SessionLocal
from app.dependencies import get_current_user
from app.models.user import User
from typing import List
from app.schemas.answer import AnswerOut
from app.services.crud_answer import get_answers_by_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit-answer")
def submit_checkin_answer(
    payload: CheckinAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    saved = create_answer(db, payload, user_id=current_user.id)
    return {
        "message": "Answer saved",
        "user": current_user.email,
        "id": saved.id,
        "timestamp": saved.timestamp
    }

@router.get("/me/answers", response_model=List[AnswerOut])
def get_my_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_answers_by_user(db, user_id=current_user.id)