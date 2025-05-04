import os
import uuid
import logging
from pathlib import Path
from typing import Tuple

from PIL import Image

logger = logging.getLogger(__name__)

def save_upload_file(upload_file, temp_dir="temp") -> str:
    """Save an uploaded file to a temporary directory and return the file path"""
    try:
        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        file_ext = Path(upload_file.filename).suffix
        file_id = str(uuid.uuid4())
        file_path = os.path.join(temp_dir, f"{file_id}{file_ext}")

        with open(file_path, "wb") as buffer:
            contents = upload_file.file.read()
            buffer.write(contents)
            
        logger.info(f"Saved uploaded file to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise e

def load_image(path: str) -> Image.Image:
    """Load an image from a file path"""
    try:
        return Image.open(path).convert("RGB")
    except Exception as e:
        logger.error(f"Error loading image from {path}: {str(e)}")
        raise e

def get_output_path(results_dir: str, suffix=".png") -> str:
    """Generate a unique output file path"""
    try:
        Path(results_dir).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(results_dir, f"{uuid.uuid4()}{suffix}")
        logger.info(f"Generated output path: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error generating output path: {str(e)}")
        raise e
