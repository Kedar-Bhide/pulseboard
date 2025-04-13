from fastapi import APIRouter
from app.schemas.answer import CheckinAnswerCreate

router = APIRouter()

# For now, just echo back the answer — DB comes later
@router.post("/submit-answer")
def submit_checkin_answer(payload: CheckinAnswerCreate):
    return {
        "message": "Answer received",
        "question": payload.question,
        "answer": payload.answer
    }