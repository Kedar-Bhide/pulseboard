from fastapi import APIRouter, Depends, Query, HTTPException
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
from app.core.reminder import generate_nudge
from sqlalchemy import func 

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

@router.get("/admin/missed-checkins/messages")
def get_nudge_messages(db: Session = Depends(get_db)):
    users = get_users_who_didnt_checkin_today(db)
    messages = [
        {
            "user_id": u.id,
            "email": u.email,
            "message": generate_nudge(u.email.split("@")[0])  # Use name part
        }
        for u in users
    ]
    return messages

@router.get("/admin/engagement-summary")
def get_engagement_summary(db: Session = Depends(get_db)):
    users = db.query(User).all()
    today = datetime.utcnow().date()
    week_ago = datetime.utcnow() - timedelta(days=7)

    summary = []

    for user in users:
        answers = get_answers_by_user(db, user.id)
        total = len(answers)
        last = answers[0].timestamp.date() if answers else None

        # Streak calc
        dates = sorted({a.timestamp.date() for a in answers})
        streak = 1
        for i in range(len(dates) - 2, -1, -1):
            if (dates[i + 1] - dates[i]).days == 1:
                streak += 1
            else:
                break

        current_streak = streak if dates and dates[-1] in [today, today - timedelta(days=1)] else 0

        # Today’s check-in?
        has_checked_in_today = any(a.timestamp.date() == today for a in answers)

        summary.append({
            "user": user.email,
            "slack_id": user.slack_id,
            "total_checkins": total,
            "last_checkin": last.isoformat() if last else None,
            "current_streak": current_streak,
            "checked_in_today": has_checked_in_today
        })

    return summary

@router.get("/admin/user-answers")
def get_user_answers(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    answers = get_answers_by_user(db, user_id=user.id)
    return [
        {
            "id": a.id,
            "question": a.question.content if a.question else "N/A",
            "answer": a.answer,
            "timestamp": a.timestamp
        } for a in answers
    ]

@router.get("/admin/weekly-summary")
def get_weekly_summary(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    week_ago = datetime.utcnow() - timedelta(days=7)
    answers = (
        db.query(Answer)
        .filter(Answer.user_id == user.id)
        .filter(Answer.timestamp >= week_ago)
        .order_by(Answer.timestamp.asc())
        .all()
    )

    summary = generate_weekly_summary(answers)
    return {"summary": summary}

@router.get("/admin/team-summaries")
def get_team_summaries(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.slack_id.isnot(None)).all()
    week_ago = datetime.utcnow() - timedelta(days=7)
    summaries = []

    for user in users:
        answers = (
            db.query(Answer)
            .filter(Answer.user_id == user.id)
            .filter(Answer.timestamp >= week_ago)
            .order_by(Answer.timestamp.asc())
            .all()
        )
        if answers:
            summary = generate_weekly_summary(answers)
            summaries.append(f"{user.email}\n{summary}\n\n")

    return {"full_summary": "\n".join(summaries)}

# @router.get("/admin/user-activity")
# def get_user_activity(email: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     today = datetime.utcnow().date()
#     days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # 7 days, oldest to newest

#     activity = []
#     for day in days:
#         exists = (
#             db.query(Answer)
#             .filter(Answer.user_id == user.id)
#             .filter(func.date(Answer.timestamp) == day)
#             .first()
#         )
#         activity.append(1 if exists else 0)

#     return {"activity": activity}

@router.get("/admin/batch-activity")
def get_batch_activity(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.slack_id.isnot(None)).all()
    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    result = {}

    for user in users:
        activity = []
        for day in days:
            exists = (
                db.query(Answer)
                .filter(Answer.user_id == user.id)
                .filter(func.date(Answer.timestamp) == day)
                .first()
            )
            activity.append(1 if exists else 0)
        result[user.email] = activity

    return {"activity": result}