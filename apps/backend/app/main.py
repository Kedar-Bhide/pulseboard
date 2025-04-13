from fastapi import FastAPI
from app.api.v1 import questions, answers

app = FastAPI()

app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Pulseboard!"}