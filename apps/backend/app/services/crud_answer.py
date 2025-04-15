from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import CheckinAnswerCreate
from typing import List

def create_answer(db: Session, answer_data: CheckinAnswerCreate, user_id: int) -> Answer:
    db_answer = Answer(
        question=answer_data.question,
        answer=answer_data.answer,
        user_id=user_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answers_by_user(db: Session, user_id: int) -> List[Answer]:
    return (
        db.query(Answer)
        .filter(Answer.user_id == user_id)
        .order_by(Answer.timestamp.desc())
        .all()
    )