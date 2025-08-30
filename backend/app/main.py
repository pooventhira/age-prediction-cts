# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import prediction
from app.core.config import settings
from app.core.exceptions import add_exception_handlers

app = FastAPI(
    title="Age Prediction API",
    description="API for predicting age from multi-angle facial images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add custom exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])

@app.get("/")
async def root():
    return {"message": "Age Prediction API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "age-prediction-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
