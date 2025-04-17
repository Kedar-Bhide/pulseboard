from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.answer import CheckinAnswerCreate, AnswerOut
from app.services.crud_answer import create_answer
from app.database import SessionLocal
from app.dependencies import get_current_user
from app.models.user import User
from typing import List
from app.services.crud_answer import get_answers_by_user
from datetime import datetime, timedelta
from app.core.summary import generate_weekly_summary
from app.models.answer import Answer
from app.services.analytics import get_users_who_didnt_checkin_today

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
        "question_id": saved.question_id,
        "timestamp": saved.timestamp
    }

@router.get("/me/answers", response_model=List[AnswerOut])
def get_my_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: str = Query(default=None, description="Search term")
):
    answers = get_answers_by_user(db, user_id=current_user.id)

    if q:
        q_lower = q.lower()
        answers = [
            a for a in answers
            if q_lower in a.answer.lower() or (a.question and q_lower in a.question.content.lower())
        ]

    return [
        AnswerOut(
            id=a.id,
            answer=a.answer,
            timestamp=a.timestamp,
            question=a.question.content if a.question else "N/A"
        ) for a in answers
    ]

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

@router.get("/me/stats")
def get_checkin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_answers = get_answers_by_user(db, current_user.id)
    total = len(all_answers)

    if total == 0:
        return {
            "total": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_checkin": None,
        }

    # Extract just the date parts
    dates = sorted({a.timestamp.date() for a in all_answers})
    last_checkin = dates[-1]

    # Calculate streaks
    from datetime import timedelta
    streak = 1
    longest_streak = 1

    for i in range(len(dates) - 2, -1, -1):
        delta = (dates[i + 1] - dates[i]).days
        if delta == 1:
            streak += 1
            longest_streak = max(longest_streak, streak)
        elif delta > 1:
            break

    today = datetime.utcnow().date()
    current_streak = streak if dates[-1] == today or dates[-1] == today - timedelta(days=1) else 0

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_checkin": last_checkin.isoformat()
    }

@router.get("/admin/missed-checkins")
def get_users_who_missed_today(db: Session = Depends(get_db)):
    users = get_users_who_didnt_checkin_today(db)
    return [{"id": u.id, "email": u.email} for u in users]