from app.models.answer import Answer
from app.core.gpt import ask_openai

def generate_weekly_summary(answers: list[Answer]) -> str:
    if not answers:
        return "No check-ins submitted this week."

    content = "\n".join(
        [f"Q: {a.question}\nA: {a.answer}" for a in answers]
    )

    prompt = (
        "You're a thoughtful startup advisor.\n"
        "Summarize the following week of daily check-in responses. "
        "Highlight themes, risks, emotions, and momentum. Use 3–4 bullet points.\n\n"
        f"{content}"
    )

    return ask_openai(prompt)