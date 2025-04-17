from fastapi import FastAPI
from app.api.v1 import questions, answers, slack
from app.database import Base, engine
from app.api.v1 import auth
from app.core.scheduler import start_scheduler
from app.models import answer, user, question

# Create DB tables (only on startup for now)
Base.metadata.create_all(bind=engine)

app = FastAPI()
start_scheduler()

# Register routers
app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(slack.router, prefix="/api/v1/slack")

@app.get("/")
def read_root():
    return {"message": "Welcome to Pulseboard!"}