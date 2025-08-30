# app/services/ml_service.py
import pickle
import numpy as np
from typing import List, Dict
from pathlib import Path
import logging
from app.core.exceptions import ModelLoadError, PredictionError
from app.core.config import settings

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the pickled age prediction model"""
        try:
            model_path = Path(settings.model_path)
            if not model_path.exists():
                raise ModelLoadError(f"Model file not found at {model_path}")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            logger.info(f"Model loaded successfully from {model_path}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise ModelLoadError(f"Failed to load model: {str(e)}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None
    
    def predict_age(self, processed_images: List[np.ndarray]) -> Dict:
        """
        Predict age from processed images
        
        Args:
            processed_images: List of preprocessed image arrays [front, left_side, right_side]
            
        Returns:
            Dict with 'age' and 'confidence' keys
        """
        if not self.is_model_loaded():
            raise PredictionError("Model not loaded")
        
        try:
            # Extract features from multi-angle images
            features = self._extract_features(processed_images)
            
            # Get prediction from model
            prediction = self.model.predict([features])[0]
            confidence = self._calculate_confidence(features)
            
            # Ensure age is within reasonable bounds
            predicted_age = max(1, min(120, int(prediction)))
            
            return {
                "age": predicted_age,
                "confidence": float(confidence)
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise PredictionError(f"Prediction failed: {str(e)}")
    
    def _extract_features(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Extract features from multi-angle images for model input
        
        TODO: Implement based on your specific model requirements
        This is a placeholder that you'll need to customize based on how 
        your pickle model was trained and what features it expects
        """
        # Example implementation - customize based on your model
        try:
            # Option 1: Use primary (front) image
            primary_image = images[0]  # front view
            features = primary_image.flatten()
            
            # Option 2: Combine all images (if your model supports this)
            # combined = np.concatenate([img.flatten() for img in images])
            # features = combined
            
            # Option 3: Average the images
            # averaged = np.mean(images, axis=0)
            # features = averaged.flatten()
            
            return features
            
        except Exception as e:
            raise PredictionError(f"Feature extraction failed: {str(e)}")
    
    def _calculate_confidence(self, features: np.ndarray) -> float:
        """
        Calculate confidence score for the prediction
        
        TODO: Implement based on your model's capabilities
        """
        try:
            # Option 1: If your model has predict_proba method
            # if hasattr(self.model, 'predict_proba'):
            #     probabilities = self.model.predict_proba([features])[0]
            #     confidence = np.max(probabilities)
            
            # Option 2: Simple confidence based on feature quality
            # You can implement custom logic here
            confidence = 0.85  # Placeholder - implement your logic
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.warning(f"Confidence calculation failed: {str(e)}")
            return 0.5  # Default moderate confidence
