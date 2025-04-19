from app.models.answer import Answer
from app.core.gpt import ask_openai

def generate_weekly_summary(answers: list[Answer]) -> str:
    if not answers:
        return "No check-ins submitted this week."

    content = "\n".join([f"Q: {a.question.content}\nA: {a.answer}" for a in answers if a.question])

    prompt = (
        "You're a reflective coach summarizing a startup founder's weekly check-ins.\n"
        "Summarize the insights, patterns, and blockers in 3-4 concise bullet points.\n\n"
        f"{content}"
    )

    return ask_openai(prompt)