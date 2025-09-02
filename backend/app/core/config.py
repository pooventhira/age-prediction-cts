from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Age Prediction API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Model
    MODEL_PATH: str = "app/model/age_predictor.h5"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # --- New Database and Auth Settings ---
    MONGODB_URL: str
    DB_NAME: str = "AgePredictionDB"
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
