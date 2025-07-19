import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def ask_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for startup founders."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message["content"]