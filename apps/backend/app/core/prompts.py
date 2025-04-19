from app.core.gpt import ask_openai
from app.services.crud_question import create_question
from app.database import SessionLocal
from app.services.analytics import get_users_who_didnt_checkin_today
from app.core.reminder import generate_nudge
from app.core.slack import send_slack_dm
from app.models.user import User
from app.services.crud_answer import get_answers_by_user
from app.core.summary import generate_weekly_summary
from app.core.slack import send_slack_dm
from datetime import datetime, timedelta
from app.models.answer import Answer

def generate_and_log_question():
    prompt = (
        "Generate one thoughtful check-in question for a startup team. "
        "Keep it relevant to team dynamics, product, or founder clarity."
    )
    question_text = ask_openai(prompt)

    db = SessionLocal()
    create_question(db, question_text)
    db.close()

    print(f"✅ Daily question saved: {question_text}")

def send_missed_checkin_reminders():
    db = SessionLocal()
    users = get_users_who_didnt_checkin_today(db)

    for user in users:
        if user.slack_id:
            message = generate_nudge(user.email.split("@")[0])
            send_slack_dm(user.slack_id, message, include_button=True)
            print(f"Sent reminder to {user.email}")
    db.close()

def send_weekly_summaries():
    db = SessionLocal()
    users = db.query(User).filter(User.slack_id.isnot(None)).all()
    week_ago = datetime.utcnow() - timedelta(days=7)

    for user in users:
        answers = (
            db.query(Answer)
            .filter(Answer.user_id == user.id)
            .filter(Answer.timestamp >= week_ago)
            .order_by(Answer.timestamp.asc())
            .all()
        )

        summary = generate_weekly_summary(answers)
        send_slack_dm(user.slack_id, f"🧠 *Your Weekly Check-In Summary:*\n{summary}")

    db.close()