from app.core.gpt import ask_openai
from app.services.crud_question import create_question
from app.database import SessionLocal

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