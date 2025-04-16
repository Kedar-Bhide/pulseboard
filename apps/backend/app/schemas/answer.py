from pydantic import BaseModel
from datetime import datetime

class CheckinAnswerCreate(BaseModel):
    question_id: int
    answer: str

class AnswerOut(BaseModel):
    id: int
    answer: str
    timestamp: datetime
    question: str  
    
    class Config:
        orm_mode = True