from pydantic import BaseModel
from typing import Optional

class PredictionResponse(BaseModel):
    """Response schema for age prediction"""
    age: int
    confidence: Optional[float] = None
    message: str = "Age prediction successful"
    
    class Config:
        schema_extra = {
            "example": {
                "age": 25,
                "confidence": 0.85,
                "message": "Age prediction successful"
            }
        }

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: str
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Invalid image format"
            }
        }

class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    service: str
