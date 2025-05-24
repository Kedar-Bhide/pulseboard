from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    team_id: Optional[int] = None
    role: Optional[str] = "member"
    timezone: Optional[str] = "UTC"

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=8)
    full_name: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[constr(min_length=8)] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_checkin: Optional[datetime] = None
    current_streak: int
    total_checkins: int

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None