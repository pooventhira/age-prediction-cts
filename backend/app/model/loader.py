import tensorflow as tf
from tensorflow import keras
import os
from pathlib import Path
from app.core.config import settings
import logging
import numpy as np

logger = logging.getLogger(__name__)

def load_model():
    """
    Load the pre-trained Keras age prediction model.
    For now, returns a mock model since we don't have a real .h5 file.
    """
    model_path = Path(settings.MODEL_PATH)
    
    try:
        if model_path.exists():
            model = keras.models.load_model(model_path)
            logger.info(f"Keras model loaded successfully from {model_path}")
            return model
        else:
            logger.warning(f"Model file not found at {model_path}. Using mock model.")
            return MockKerasAgePredictor()
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}. Using mock model.")
        return MockKerasAgePredictor()

class MockKerasAgePredictor:
    """
    Mock Keras model for demonstration purposes.
    Replace this with your actual trained model.
    """
    
    def __init__(self):
        """Initialize mock model with expected input shape"""
        self.input_shape = (224, 224, 3)
        self.model_name = "MockAgePredictor"
    
    def predict(self, image_array):
        """
        Mock prediction method that mimics Keras model.predict()
        
        Args:
            image_array: Preprocessed image array with shape (batch_size, height, width, channels)
            
        Returns:
            numpy array with predicted age
        """
        import random
        
        # Ensure input has batch dimension
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        batch_size = image_array.shape[0]
        
        # Mock prediction - return random ages for each image in batch
        predictions = []
        for _ in range(batch_size):
            age = random.randint(18, 65)
            predictions.append([age])  # Keras typically returns 2D array
            
        return np.array(predictions, dtype=np.float32)
    
    def predict_with_confidence(self, image_array):
        """
        Mock prediction with confidence score.
        This method is custom and won't exist in real Keras models.
        """
        predictions = self.predict(image_array)
        age = int(predictions[0][0])
        
        # Mock confidence calculation
        import random
        confidence = random.uniform(0.7, 0.95)
        
        return age, confidence
    
    @property
    def input_shape_info(self):
        """Return expected input shape"""
        return self.input_shape
