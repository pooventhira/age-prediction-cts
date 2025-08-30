# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class PredictionResponse(BaseModel):
    predicted_age: int = Field(..., description="Predicted age in years", ge=0, le=120)
    confidence_score: float = Field(..., description="Confidence score between 0 and 1", ge=0.0, le=1.0)
    status: str = Field(..., description="Status of the prediction")
    message: Optional[str] = Field(None, description="Additional information or error message")

    class Config:
        json_schema_extra = {
            "example": {
                "predicted_age": 25,
                "confidence_score": 0.87,
                "status": "success",
                "message": "Age prediction completed successfully"
            }
        }

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ImageProcessingError",
                "message": "Invalid image format or corrupted file"
            }
        }
