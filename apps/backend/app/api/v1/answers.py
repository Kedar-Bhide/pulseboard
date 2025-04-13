from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.answer import CheckinAnswerCreate
from app.services.crud_answer import create_answer
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit-answer")
def submit_checkin_answer(payload: CheckinAnswerCreate, db: Session = Depends(get_db)):
    saved = create_answer(db, payload)
    return {
        "message": "Answer saved",
        "id": saved.id,
        "timestamp": saved.timestamp
    }