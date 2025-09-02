from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.prediction import router as prediction_router
from app.api.auth import router as auth_router
from app.api.history import router as history_router # <-- Import the new router
from app.model.loader import load_model

# Load model on startup
model = load_model()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A FastAPI service for age prediction from images",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"], # <-- Add DELETE method
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(history_router, prefix="/api/v1/history", tags=["History"]) # <-- Add the new router

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# ... (health_check and uvicorn.run remain the same)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
