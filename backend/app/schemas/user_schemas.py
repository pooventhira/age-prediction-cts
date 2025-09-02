from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- History ---
class HistoryItem(BaseModel):
    image_base64: str
    predicted_age: int
    created_at: datetime = datetime.now()

# --- User ---
class UserBase(BaseModel):
    email: EmailStr

class UserInDB(UserBase):
    hashed_password: str
    history: List[HistoryItem] = []

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
