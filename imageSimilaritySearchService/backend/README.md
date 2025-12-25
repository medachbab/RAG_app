# FastAPI backend for Image Similarity Service

This folder contains a FastAPI backend around the image retrieval system.

Quick start (local Python):

1. Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r ../requirements.txt
```

2. Run the API with uvicorn:

```bash
uvicorn fastApi.main:app --host 0.0.0.0 --port 8000
```

Notes:
- The service serves images from `products_images/` under `/images`.
- Use `POST /search` with form-data `file` to search by image.
- There is a `GET /health` endpoint for quick status checks.
