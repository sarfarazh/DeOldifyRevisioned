from pydantic import BaseModel, Field

class ColorizationResult(BaseModel):
    """Model for colorization result response"""
    output_path: str = Field(description="Path to the colorized image")
    message: str = Field(description="Status message")
