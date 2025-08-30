# app/services/image_service.py
import cv2
import numpy as np
from fastapi import UploadFile, HTTPException
from typing import List
import io
from PIL import Image
import logging
from app.core.config import settings
from app.core.exceptions import ImageProcessingError

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        # Adjust these based on your model requirements
        self.target_size = (224, 224)
        self.min_face_size = (50, 50)
    
    async def validate_uploaded_files(self, files: List[UploadFile]):
        """Validate uploaded image files"""
        if len(files) != 3:
            raise ImageProcessingError("Exactly 3 images required: front, left_side, right_side")
        
        for i, file in enumerate(files):
            # Check file size
            if file.size > settings.max_file_size:
                raise ImageProcessingError(f"Image {i+1} too large. Max size: {settings.max_file_size} bytes")
            
            # Check file type
            if file.content_type not in settings.supported_image_types:
                raise ImageProcessingError(f"Unsupported image type: {file.content_type}")
    
    async def process_multi_angle_images(self, files: List[UploadFile]) -> List[np.ndarray]:
        """Process uploaded images for ML model input"""
        processed_images = []
        
        try:
            for i, file in enumerate(files):
                logger.info(f"Processing image {i+1}: {file.filename}")
                
                # Read image content
                content = await file.read()
                if len(content) == 0:
                    raise ImageProcessingError(f"Image {i+1} is empty")
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(content))
                
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Basic validation
                if image.size[0] < 100 or image.size[1] < 100:
                    raise ImageProcessingError(f"Image {i+1} too small. Minimum size: 100x100")
                
                # Resize to target size
                image = image.resize(self.target_size, Image.Resampling.LANCZOS)
                
                # Convert to numpy array and normalize
                image_array = np.array(image, dtype=np.float32) / 255.0
                
                # Validate processed image
                if not self._validate_processed_image(image_array):
                    raise ImageProcessingError(f"Image {i+1} failed quality validation")
                
                processed_images.append(image_array)
                logger.info(f"Successfully processed image {i+1}")
            
            return processed_images
            
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise ImageProcessingError(f"Image processing failed: {str(e)}")
    
    def _validate_processed_image(self, image_array: np.ndarray) -> bool:
        """Basic validation of processed image"""
        try:
            # Check array shape
            if len(image_array.shape) != 3 or image_array.shape[2] != 3:
                return False
            
            # Check value range (should be 0-1 after normalization)
            if image_array.min() < 0 or image_array.max() > 1:
                return False
            
            # Check for completely black or white images
            mean_value = np.mean(image_array)
            if mean_value < 0.01 or mean_value > 0.99:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            return False
    
    def detect_face(self, image_array: np.ndarray) -> bool:
        """
        Optional: Detect if image contains a face
        Uncomment and customize if you want face detection
        """
        try:
            # Convert back to uint8 for OpenCV
            img_uint8 = (image_array * 255).astype(np.uint8)
            gray = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2GRAY)
            
            # Load face cascade (you'll need to download the XML file)
            # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # return len(faces) > 0
            
            # Placeholder - always return True for now
            return True
            
        except Exception as e:
            logger.warning(f"Face detection failed: {str(e)}")
            return True  # Don't fail if face detection has issues
