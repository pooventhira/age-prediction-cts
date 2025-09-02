from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from typing import Optional
from app.schemas.response_schemas import PredictionResponse, ErrorResponse
from app.schemas.user_schemas import UserInDB
from app.services.prediction_service import prediction_service
from app.core.security import get_current_user_optional, validate_file_size, validate_image_format
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Age Prediction"])

@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Predict age from image",
    description="Upload an image to predict age. If authenticated, the result is saved to your history."
)
async def predict_age(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, WebP)"),
    current_user: Optional[UserInDB] = Depends(get_current_user_optional)
):
    """
    Predicts age from an uploaded image.
    - **file**: Image file to analyze (max 10MB).
    - An optional **Authorization: Bearer <token>** header can be provided.
    """
    if not validate_image_format(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Supported types: JPEG, PNG, WebP"
        )
    
    try:
        file_content = await file.read()
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error reading uploaded file")
    
    if not validate_file_size(len(file_content), settings.MAX_FILE_SIZE):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    try:
        # Pass the optional user object to the service layer
        predicted_age, confidence = await prediction_service.predict_age(file_content, current_user)
        
        return PredictionResponse(
            age=predicted_age,
            confidence=round(confidence, 2),
            message="Age prediction successful"
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# The /model/info endpoint remains unchanged
@router.get("/model/info", summary="Get model information")
async def get_model_info():
    # ... (code for this endpoint is unchanged)
    return {"model_path": settings.MODEL_PATH}
