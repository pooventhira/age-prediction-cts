# app/api/prediction.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List
from app.models.schemas import PredictionResponse, ErrorResponse
from app.services.ml_service import MLService
from app.services.image_service import ImageService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency injection for services
def get_ml_service():
    return MLService()

def get_image_service():
    return ImageService()

@router.post("/predict-age", response_model=PredictionResponse)
async def predict_age(
    front_view: UploadFile = File(..., description="Front view image"),
    left_side: UploadFile = File(..., description="Left side view image"),
    right_side: UploadFile = File(..., description="Right side view image"),
    ml_service: MLService = Depends(get_ml_service),
    image_service: ImageService = Depends(get_image_service)
):
    """
    Predict age from multi-angle facial images
    
    Expects 3 images:
    - front_view: Front-facing image
    - left_side: Left side profile
    - right_side: Right side profile
    
    Returns predicted age and confidence score
    """
    try:
        # Validate file types and sizes
        files = [front_view, left_side, right_side]
        await image_service.validate_uploaded_files(files)
        
        logger.info(f"Processing age prediction request with {len(files)} images")
        
        # Process images
        processed_images = await image_service.process_multi_angle_images(files)
        
        # Get prediction from ML model
        result = ml_service.predict_age(processed_images)
        
        logger.info(f"Prediction successful: age={result['age']}, confidence={result['confidence']}")
        
        return PredictionResponse(
            predicted_age=result["age"],
            confidence_score=result["confidence"],
            status="success",
            message="Age prediction completed successfully"
        )
        
    except Exception as e:
        logger.error(f"Age prediction failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@router.get("/model-status")
async def model_status(ml_service: MLService = Depends(get_ml_service)):
    """Check if the ML model is loaded and ready"""
    is_loaded = ml_service.is_model_loaded()
    return {
        "model_loaded": is_loaded,
        "model_path": settings.model_path,
        "status": "ready" if is_loaded else "error"
    }
