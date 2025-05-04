# DeOldifyRevisioned

> 🧠 A modern, actively maintained extension of [DeOldify](https://github.com/jantic/DeOldify), which was archived in October 2024.

This project continues DeOldify's mission to bring color to old black-and-white photos and videos using state-of-the-art AI, with additional features including a FastAPI interface for easy integration.

## 🔗 Original Project Reference

- Original Author: Jason Antic  
- Archived Repo: [https://github.com/jantic/DeOldify](https://github.com/jantic/DeOldify)  
- License: MIT  

## ✨ Features

- **AI-Powered Colorization**: Transform black and white photos into colorized versions
- **Two Colorization Models**: 
  - **Artistic**: More vibrant colors, good for artistic renderings
  - **Stable**: More consistent colorization, better for portraits and landscapes
- **FastAPI Interface**: Easy-to-use REST API for integration into other applications
- **Adjustable Quality Settings**: Configure render quality based on your hardware capabilities

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended 4GB+ VRAM)
- WSL2 or Linux environment

### Setting Up the Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/sarfarazh/DeOldifyRevisioned.git
   cd DeOldifyRevisioned
   ```

2. Create and activate a conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate deoldify
   ```

3. Download pre-trained model weights:
   ```bash
   mkdir -p models
   # For artistic model (default)
   wget https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth
   # For stable model (optional)
   # wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth -O ./models/ColorizeStable_gen.pth
   ```

### Running the Jupyter Notebooks

For interactive colorization:

```bash
jupyter lab
```

Then open either:
- `ImageColorizer.ipynb` for image colorization
- `VideoColorizer.ipynb` for video colorization

## 🚀 Using the FastAPI Interface

### Starting the API Server

```bash
# Install API-specific dependencies
pip install -r requirements-api.txt

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with Swagger documentation at `http://localhost:8000/docs`.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check/status |
| `/test` | GET | Test colorization with a sample image |
| `/colorize` | POST | Colorize an uploaded black and white image |
| `/results/{filename}` | GET | Retrieve a colorized image result |

### Example Usage

Using cURL:

```bash
# Colorize an image
curl -X POST "http://localhost:8000/colorize" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/bw-image.jpg"
```

Using Python requests:

```python
import requests

# Colorize an image
url = "http://localhost:8000/colorize"
files = {"file": open("path/to/your/bw-image.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()
```

## ⚙️ Configuration

Configure the API via environment variables or by editing `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_TYPE` | Model type (artistic or stable) | artistic |
| `MODEL_WEIGHTS_PATH` | Path to model weights file | models/ColorizeArtistic_gen.pth |
| `RENDER_FACTOR` | Rendering quality (10-45) | 20 |
| `RESULTS_DIR` | Directory to store colorized images | outputs |

## 💻 Hardware Considerations

- **Minimum**: CUDA-compatible GPU with 4GB VRAM
- **Recommended**: GPU with 8GB+ VRAM
- **CPU-only**: Supported but significantly slower

For devices with limited VRAM (4GB):
- Set render_factor to 15-20 for images
- Set render_factor to 10-15 for videos

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- [Jason Antic](https://github.com/jantic) for the original DeOldify project
- The fastai community for their tools and support
