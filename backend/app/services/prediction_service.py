from PIL import Image
import numpy as np
import io
from typing import Tuple
import logging
from app.model.loader import load_model
import tensorflow as tf

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model = load_model()
    
    async def predict_age(self, image_bytes: bytes) -> Tuple[int, float]:
        """
        Process image and predict age using Keras model.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Tuple of (predicted_age, confidence_score)
        """
        try:
            # Preprocess image for Keras model
            processed_image = await self._preprocess_image(image_bytes)
            
            # Make prediction using Keras model
            if hasattr(self.model, 'predict_with_confidence'):
                # Use mock method if available
                age, confidence = self.model.predict_with_confidence(processed_image)
            else:
                # Standard Keras model prediction
                predictions = self.model.predict(processed_image, verbose=0)
                
                # Extract age from prediction
                # Assuming model outputs single value (age) or needs post-processing
                if len(predictions.shape) > 1 and predictions.shape[1] == 1:
                    age = float(predictions[0][0])
                else:
                    age = float(predictions[0]) if len(predictions.shape) == 1 else float(predictions[0][0])
                
                # Calculate confidence (you may want to modify this based on your model)
                confidence = self._calculate_confidence(predictions)
            
            return int(max(0, age)), float(confidence)
            
        except Exception as e:
            logger.error(f"Error in age prediction: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")
    
    async def _preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess the input image for Keras model inference.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Processed image as numpy array with batch dimension
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to expected input size (typical for age prediction models)
            target_size = (64, 64)  # Most common size, adjust based on your model
            image = image.resize(target_size)
            
            # Convert to numpy array
            image_array = np.array(image, dtype=np.float32)
            
            # Normalize pixel values to [0,1] range (standard for most models)
            image_array = image_array / 255.0
            
            # Add batch dimension: (height, width, channels) -> (1, height, width, channels)
            image_array = np.expand_dims(image_array, axis=0)
            
            logger.info(f"Preprocessed image shape: {image_array.shape}")
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise ValueError("Invalid image format or corrupted image")
    
    def _calculate_confidence(self, predictions: np.ndarray) -> float:
        """
        Calculate confidence score from model predictions.
        This is a simple implementation - you may want to modify based on your model architecture.
        
        Args:
            predictions: Raw predictions from the model
            
        Returns:
            Confidence score between 0 and 1
        """
        try:
            # For regression models (direct age output), confidence can be based on:
            # 1. Inverse of prediction variance (if model outputs uncertainty)
            # 2. Distance from mean age
            # 3. Model-specific confidence measures
            
            # Simple confidence calculation (you may want to improve this)
            # For now, return a fixed confidence - improve based on your model's output
            if hasattr(self.model, 'predict_proba'):
                # If model has probability output
                confidence = np.max(predictions)
            else:
                # For regression models, use a simple heuristic
                # You might want to use model uncertainty or other metrics
                confidence = 0.85  # Default confidence
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.warning(f"Error calculating confidence: {str(e)}")
            return 0.80  # Default confidence
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        try:
            if hasattr(self.model, 'input_shape'):
                input_shape = self.model.input_shape
            elif hasattr(self.model, 'input_shape_info'):
                input_shape = self.model.input_shape_info
            else:
                input_shape = "Unknown"
                
            if hasattr(self.model, 'summary'):
                # Real Keras model
                return {
                    "model_type": "Keras/TensorFlow",
                    "input_shape": input_shape,
                    "framework": "TensorFlow",
                    "is_mock": False
                }
            else:
                # Mock model
                return {
                    "model_type": "Mock Keras Model",
                    "input_shape": input_shape,
                    "framework": "Mock",
                    "is_mock": True
                }
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {
                "model_type": "Unknown",
                "error": str(e),
                "is_mock": True
            }

# Create singleton instance
prediction_service = PredictionService()
