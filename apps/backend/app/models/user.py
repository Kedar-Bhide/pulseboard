from sqlalchemy import Boolean, Column, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Team related fields
    team_id = Column(Integer, nullable=True)
    role = Column(String, default="member")  # member, admin, owner
    timezone = Column(String, default="UTC")
    
    # Check-in related fields
    last_checkin = Column(DateTime(timezone=True), nullable=True)
    current_streak = Column(Integer, default=0)
    total_checkins = Column(Integer, default=0)
    
    answers = relationship("Answer", back_populates="user")
    slack_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"