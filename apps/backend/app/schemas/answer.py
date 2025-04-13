from pydantic import BaseModel

class CheckinAnswerCreate(BaseModel):
    question: str
    answer: str