from pydantic import BaseModel
from datetime import datetime

class QuestionOut(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True