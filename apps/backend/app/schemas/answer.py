from pydantic import BaseModel
from datetime import datetime

class CheckinAnswerCreate(BaseModel):
    question_id: int
    answer: str

class AnswerOut(BaseModel):
    id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        orm_mode = True