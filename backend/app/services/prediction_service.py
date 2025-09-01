from PIL import Image
import numpy as np
import io
from typing import Tuple
import logging
from app.model.loader import load_model

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model = load_model()
    
    async def predict_age(self, image_bytes: bytes) -> Tuple[int, float]:
        """
        Process image and predict age.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Tuple of (predicted_age, confidence_score)
        """
        try:
            # Preprocess image
            processed_image = await self._preprocess_image(image_bytes)
            
            # Extract features (mock implementation)
            features = self._extract_features(processed_image)
            
            # Make prediction
            if hasattr(self.model, 'predict_with_confidence'):
                age, confidence = self.model.predict_with_confidence(features)
            else:
                age = self.model.predict(features)
                confidence = 0.80  # Default confidence
            
            return int(age), float(confidence)
            
        except Exception as e:
            logger.error(f"Error in age prediction: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")
    
    async def _preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess the input image for model inference.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Processed image as numpy array
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image (common preprocessing step)
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32)
            image_array = image_array / 255.0
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise ValueError("Invalid image format or corrupted image")
    
    def _extract_features(self, image_array: np.ndarray) -> np.ndarray:
        """
        Extract features from preprocessed image.
        This is a mock implementation - replace with actual feature extraction.
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            Feature vector
        """
        # Mock feature extraction - flatten and take mean
        # In real implementation, this would use CNN features or other methods
        features = np.mean(image_array.reshape(-1, image_array.shape[-1]), axis=0)
        return features

# Create singleton instance
prediction_service = PredictionService()
