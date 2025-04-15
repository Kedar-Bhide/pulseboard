from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import CheckinAnswerCreate

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