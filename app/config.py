import os
import logging
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Literal

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseModel):
    """Application settings"""
    # Model configuration
    model_type: Literal["artistic", "stable"] = Field(
        default=os.getenv("MODEL_TYPE", "artistic"),
        description="Model type to use for colorization (artistic or stable)"
    )
    
    # Model paths - default to project's models directory
    model_weights_path: str = Field(
        default=os.getenv("MODEL_WEIGHTS_PATH", "models/ColorizeArtistic_gen.pth"),
        description="Path to the model weights file"
    )
    
    # Rendering parameters
    render_factor: int = Field(
        default=int(os.getenv("RENDER_FACTOR", "20")),
        description="Render factor for colorization (higher is better quality but needs more VRAM)",
        ge=10,
        le=45
    )
    
    # Directory settings
    results_dir: str = Field(
        default=os.getenv("RESULTS_DIR", "outputs"),
        description="Directory to store colorized results"
    )
    
    # Model configuration helper properties
    @property
    def is_artistic(self) -> bool:
        return self.model_type == "artistic"
    
    @property
    def model_file(self) -> str:
        if self.is_artistic:
            return "ColorizeArtistic_gen.pth"
        return "ColorizeStable_gen.pth"
    
    @property
    def default_render_factor(self) -> int:
        """Get default render factor based on model type"""
        if self.is_artistic:
            return 25  # Artistic default
        return 21  # Stable default
    
    # Pydantic v2 configuration
    model_config = {"protected_namespaces": ()}

# Create settings instance
settings = Settings()

# Log configuration on startup
logger.info(f"Model type: {settings.model_type}")
logger.info(f"Model weights path: {settings.model_weights_path}")
logger.info(f"Render factor: {settings.render_factor}")
logger.info(f"Results directory: {settings.results_dir}")
