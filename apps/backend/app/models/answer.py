from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)