from fastapi import FastAPI
from app.api.v1 import questions, answers
from app.database import Base, engine
from app.models import answer

# Create DB tables (only on startup for now)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Pulseboard!"}