#!/bin/bash

echo "📁 Creating FastAPI app structure in ./app"

mkdir -p app/api
mkdir -p app/services
mkdir -p app/models
mkdir -p app/utils

# Create core FastAPI entrypoint
touch app/main.py

# API endpoints
touch app/api/endpoints.py

# DeOldify wrapper logic
touch app/services/colorizer_service.py

# Pydantic models
touch app/models/color_request.py

# Utility functions
touch app/utils/file_utils.py

# .env config loader
touch app/config.py

# Optional: requirements for FastAPI app only
touch requirements-api.txt

echo "✅ FastAPI app skeleton created."
