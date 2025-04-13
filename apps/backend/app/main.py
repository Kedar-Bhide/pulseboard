from fastapi import FastAPI
from app.core.gpt import ask_openai

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Pulseboard!"}

@app.get("/gpt-test")
def gpt_test():
    prompt = "Give me 3 thoughtful daily check-in questions for a startup founder."
    result = ask_openai(prompt)
    return {"response": result}