from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.core.config import settings
from app.schemas.user_schemas import TokenData, UserInDB
from app.services.user_service import user_service # This import is now safe

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token", auto_error=False)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserInDB]:
    """
    Dependency to get the current user from a token. Returns None if no token is provided
    or if the token is invalid, allowing for optional authentication.
    """
    if token is None:
        return None
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        token_data = TokenData(email=email)
    except JWTError:
        return None
        
    user = user_service.get_user_by_email(email=token_data.email)
    if user is None:
        return None
    
    return user

# --- Existing Validation Functions ---
def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate uploaded file size"""
    return file_size <= max_size

def validate_image_format(content_type: str) -> bool:
    """Validate image format"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    return content_type.lower() in allowed_types
