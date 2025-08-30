from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    pass

class ImageProcessingError(Exception):
    pass

class PredictionError(Exception):
    pass

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "message": "Invalid input data provided"}
    )

async def model_load_exception_handler(request: Request, exc: ModelLoadError):
    logger.error(f"Model loading error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Model Error", "message": "Failed to load prediction model"}
    )

async def image_processing_exception_handler(request: Request, exc: ImageProcessingError):
    logger.error(f"Image processing error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": "Image Processing Error", "message": str(exc)}
    )

async def prediction_exception_handler(request: Request, exc: PredictionError):
    logger.error(f"Prediction error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Prediction Error", "message": "Failed to generate age prediction"}
    )

def add_exception_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ModelLoadError, model_load_exception_handler)
    app.add_exception_handler(ImageProcessingError, image_processing_exception_handler)
    app.add_exception_handler(PredictionError, prediction_exception_handler)
