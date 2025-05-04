import os
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from app.services.colorizer_service import DeOldifyService
from app.models.color_request import ColorizationResult
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
service = DeOldifyService()

@router.get("/test", response_model=ColorizationResult)
async def test_colorizer():
    """Test endpoint that colorizes a sample image from test_images folder"""
    try:
        # Check if test_images directory exists and has files
        if not os.path.exists("test_images"):
            os.makedirs("test_images", exist_ok=True)
            return JSONResponse(
                status_code=404, 
                content={"error": "test_images directory not found or empty. Please add test images first."}
            )
            
        # Get first image from test_images
        test_files = [f for f in os.listdir("test_images") if f.endswith((".jpg", ".jpeg", ".png"))]
        if not test_files:
            return JSONResponse(
                status_code=404, 
                content={"error": "No test images found. Please add images to test_images directory."}
            )
            
        sample_path = os.path.join("test_images", test_files[0])
        logger.info(f"Using test image: {sample_path}")
        
        # Process image
        output_path = service.colorize_test_image(sample_path)
        
        # Extract just the filename for the response
        filename = os.path.basename(output_path)
        result_url = f"/results/{filename}"
        
        return ColorizationResult(output_path=result_url, message="Test image colorized successfully")
    except Exception as e:
        logger.error(f"Test endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/colorize", response_model=ColorizationResult)
async def colorize_image(file: UploadFile = File(...)):
    """Colorize an uploaded black and white image"""
    if not file.filename:
        logger.error("No file uploaded")
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only JPG, JPEG and PNG files are supported")

    try:
        logger.info(f"Processing upload: {file.filename}")
        output_path = service.colorize_image(file)
        
        # Extract just the filename for the response
        filename = os.path.basename(output_path)
        result_url = f"/results/{filename}"
        
        logger.info(f"Colorization complete: {output_path}")
        return ColorizationResult(output_path=result_url, message="Image colorized successfully")
    except Exception as e:
        logger.error(f"Colorization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{filename}")
async def get_result(filename: str):
    """Serve a colorized image result"""
    try:
        file_path = os.path.join(settings.results_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f"Result file not found: {file_path}")
            raise HTTPException(status_code=404, detail="Result not found")
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving result: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
