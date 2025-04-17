from datetime import date
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.answer import Answer

def get_users_who_didnt_checkin_today(db: Session):
    today = date.today()

    # Users who submitted an answer today
    checked_in = (
        db.query(Answer.user_id)
        .filter(Answer.timestamp >= today)
        .distinct()
        .all()
    )
    checked_in_ids = {user_id for (user_id,) in checked_in}

    # All users
    all_users = db.query(User).all()

    return [user for user in all_users if user.id not in checked_in_ids]