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
from datetime import datetime, timedelta
from app.core.summary import generate_weekly_summary
from app.models.answer import Answer

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

@router.get("/me/summary/weekly")
def get_weekly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Filter past 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_answers = (
        db.query(Answer)
        .filter(Answer.user_id == current_user.id)
        .filter(Answer.timestamp >= week_ago)
        .order_by(Answer.timestamp.asc())
        .all()
    )

    summary = generate_weekly_summary(recent_answers)
    return {"summary": summary}