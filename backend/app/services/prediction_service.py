from PIL import Image
import numpy as np
import io
import base64
from typing import Tuple, Optional
import logging
from app.model.loader import load_model
from app.schemas.user_schemas import UserInDB, HistoryItem
from app.services.user_service import user_service

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model = load_model()
    
    async def predict_age(self, image_bytes: bytes, current_user: Optional[UserInDB] = None) -> Tuple[int, float]:
        """
        Process image, predict age, and optionally save to user history.
        """
        try:
            processed_image = await self._preprocess_image(image_bytes)
            
            # --- Model prediction logic (remains the same) ---
            predictions = self.model.predict(processed_image, verbose=0)
            if len(predictions.shape) > 1 and predictions.shape[1] == 1:
                age = float(predictions[0][0])
            else:
                age = float(predictions[0])
            confidence = self._calculate_confidence(predictions)
            predicted_age = int(max(0, age))
            # --- End of prediction logic ---

            # If a user is logged in, save the result to their history
            if current_user:
                try:
                    # Create a Base64 string for storage
                    image_base64_str = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    
                    history_item = HistoryItem(
                        image_base64=image_base64_str,
                        predicted_age=predicted_age,
                    )
                    user_service.add_prediction_to_history(current_user.email, history_item)
                    logger.info(f"Saved prediction history for user: {current_user.email}")
                except Exception as e:
                    logger.error(f"Failed to save history for user {current_user.email}: {e}")

            return predicted_age, float(confidence)
            
        except Exception as e:
            logger.error(f"Error in age prediction: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")
    
    # _preprocess_image, _calculate_confidence, and get_model_info methods remain unchanged...
    async def _preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            target_size = (64, 64)
            image = image.resize(target_size)
            image_array = np.array(image, dtype=np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            return image_array
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise ValueError("Invalid image format or corrupted image")

    def _calculate_confidence(self, predictions: np.ndarray) -> float:
        return 0.85 # Placeholder confidence

    def get_model_info(self) -> dict:
        try:
            return {"input_shape": self.model.input_shape}
        except:
            return {"input_shape": "Unknown"}

# Create singleton instance
prediction_service = PredictionService()
