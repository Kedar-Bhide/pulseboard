from app.core.gpt import ask_openai

def generate_nudge(name: str) -> str:
    prompt = (
        f"You are an encouraging but honest assistant helping a startup team stay focused.\n"
        f"Write a short, motivating check-in reminder for {name} who didn’t submit their daily answer today. "
        f"Keep it casual, human, and 1-2 sentences max."
    )
    return ask_openai(prompt)