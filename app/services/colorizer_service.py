import os
import logging
from fastai.vision import load_learner
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer
from app.utils.file_utils import save_upload_file, load_image, get_output_path
from app.config import settings

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

logger = logging.getLogger(__name__)

class DeOldifyService:
    def __init__(self):
        logger.info(f"Initializing DeOldifyService with model_type=artistic (forced)")
        try:
            # Initialize device
            device.set(device=DeviceId.GPU0)
            
            # Always use artistic model since we have those weights
            logger.info("Creating colorizer with artistic=True (forced)")
            self.colorizer = get_image_colorizer(artistic=True)
            logger.info("Colorizer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing colorizer: {str(e)}")
            raise RuntimeError(f"Failed to initialize colorizer: {str(e)}")

    def colorize_test_image(self, image_path: str) -> str:
        """Test method that colorizes a sample image without file upload complexity"""
        logger.info(f"Testing colorization with image: {image_path}")
        
        try:
            # Verify the image exists
            if not os.path.exists(image_path):
                error_msg = f"Test image not found: {image_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
                
            # Generate output path
            os.makedirs(settings.results_dir, exist_ok=True)
            
            # Call colorizer with safe render factor
            render_factor = min(settings.render_factor, 20)  # Cap at 20 for 4GB GPU
            logger.info(f"Colorizing test image with render_factor={render_factor} (capped for GPU safety)")
            
            result_path = self.colorizer.plot_transformed_image(
                path=image_path,
                render_factor=render_factor,
                compare=False
            )
            
            logger.info(f"Test colorization successful: {result_path}")
            return str(result_path)
        except Exception as e:
            logger.error(f"Error in test colorization: {str(e)}")
            raise RuntimeError(f"Test colorization failed: {str(e)}")

    def colorize_image(self, upload_file) -> str:
        """Colorize an uploaded image and return the path to the colorized image"""
        try:
            # Ensure directories exist
            os.makedirs("temp", exist_ok=True)
            os.makedirs(settings.results_dir, exist_ok=True)
            
            # Save uploaded file
            logger.info(f"Processing uploaded file: {upload_file.filename}")
            input_path = save_upload_file(upload_file)
            logger.info(f"File saved at: {input_path}")
            
            # Colorize the image with safe render factor
            render_factor = min(settings.render_factor, 20)  # Cap at 20 for 4GB GPU
            logger.info(f"Colorizing with render_factor={render_factor} (capped for GPU safety)")
            
            result_path = self.colorizer.plot_transformed_image(
                path=input_path,
                render_factor=render_factor,
                compare=False
            )
            
            logger.info(f"Colorization successful: {result_path}")
            return str(result_path)
        except Exception as e:
            logger.error(f"Error during colorization: {str(e)}")
            raise RuntimeError(f"Image colorization failed: {str(e)}")
