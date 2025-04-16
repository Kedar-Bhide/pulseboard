from sqlalchemy.orm import Session
from app.models.question import Question

def create_question(db: Session, content: str) -> Question:
    question = Question(content=content)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

def get_today_question(db: Session):
    from datetime import date
    today = date.today()
    return (
        db.query(Question)
        .filter(Question.created_at >= today)
        .order_by(Question.created_at.desc())
        .first()
    )