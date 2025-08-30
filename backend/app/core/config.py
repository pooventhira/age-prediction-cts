from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Age Prediction API"
    debug: bool = False
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    max_files_per_request: int = 3
    supported_image_types: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    model_path: str = "app/models/age_predictor.pkl"
    
    class Config:
        env_file = ".env"

settings = Settings()
