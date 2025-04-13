from fastapi import APIRouter
from app.core.gpt import ask_openai

router = APIRouter()

@router.get("/checkin-question")
def get_checkin_question():
    prompt = (
        "Generate one insightful daily check-in question for a startup team. "
        "Keep it sharp, high-signal, and founder-friendly."
    )
    question = ask_openai(prompt)
    return {"question": question}