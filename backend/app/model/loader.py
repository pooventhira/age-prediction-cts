import pickle
import os
from pathlib import Path
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def load_model():
    """
    Load the pre-trained age prediction model.
    For now, returns a mock model since we don't have a real .pkl file.
    """
    model_path = Path(settings.MODEL_PATH)
    
    try:
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded successfully from {model_path}")
            return model
        else:
            logger.warning(f"Model file not found at {model_path}. Using mock model.")
            return MockAgePredictor()
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}. Using mock model.")
        return MockAgePredictor()

class MockAgePredictor:
    """
    Mock model for demonstration purposes.
    Replace this with your actual trained model.
    """
    
    def predict(self, image_features):
        """
        Mock prediction method.
        In real implementation, this would use the actual model.
        """
        # Simple mock: return a random age based on image size
        import random
        return random.randint(18, 65)
    
    def predict_with_confidence(self, image_features):
        """
        Mock prediction with confidence score.
        """
        import random
        age = random.randint(18, 65)
        confidence = random.uniform(0.7, 0.95)
        return age, confidence
