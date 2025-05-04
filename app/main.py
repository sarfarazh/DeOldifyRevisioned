import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log")
    ]
)

logger = logging.getLogger(__name__)

# Create required directories
os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("test_images", exist_ok=True)

app = FastAPI(
    title="DeOldifyRevisioned API",
    description="FastAPI wrapper for DeOldify image colorization",
    version="1.0.0"
)

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (results)
app.mount("/results", StaticFiles(directory="outputs"), name="results")

# Register routes
app.include_router(router)

# Root health check
@app.get("/")
def read_root():
    logger.info("Health check endpoint called")
    return {"status": "DeOldifyRevisioned API is live"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up DeOldifyRevisioned API")
    logger.info("Required directories created")
