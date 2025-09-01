from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os

# Security scheme for future API key implementation
security = HTTPBearer(auto_error=False)

async def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """
    Verify API key for protected endpoints.
    Currently disabled but ready for implementation.
    """
    # For now, we'll allow all requests
    # In production, implement proper API key verification
    return True

def validate_file_size(file_size: int, max_size: int = 10485760) -> bool:
    """Validate uploaded file size"""
    return file_size <= max_size

def validate_image_format(content_type: str) -> bool:
    """Validate image format"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    return content_type.lower() in allowed_types
