from fastapi import APIRouter
from app.core.gpt import ask_openai
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.question import QuestionOut
from app.services.crud_question import get_today_question
from app.database import SessionLocal

router = APIRouter()

@router.get("/checkin-question")
def get_checkin_question():
    prompt = (
        "Generate one insightful daily check-in question for a startup team. "
        "Keep it sharp, high-signal, and founder-friendly."
    )
    question = ask_openai(prompt)
    return {"question": question}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/today", response_model=QuestionOut)
def fetch_today_question(db: Session = Depends(get_db)):
    question = get_today_question(db)
    if not question:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No question for today")
    return question