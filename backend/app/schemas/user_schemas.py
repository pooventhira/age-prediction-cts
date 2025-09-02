from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

# --- History ---
class HistoryItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    image_base64: str
    predicted_age: int
    confidence: float
    created_at: datetime = Field(default_factory=datetime.now)

# --- User ---
class UserBase(BaseModel):
    email: EmailStr

class UserInDB(UserBase):
    hashed_password: str
    history: List[HistoryItem] = []

    class Config:
        orm_mode = True

# ... (rest of the file remains the same)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
