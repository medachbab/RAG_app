from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import uuid

from .retrieval_system import ImageRetrievalSystem
from .config import INDEX_PATH, METADATA_PATH

router = APIRouter()

retrieval_system = None


def get_system():
    global retrieval_system
    if retrieval_system is None:
        if not os.path.exists(INDEX_PATH):
            raise RuntimeError("Index not found. Please index images first.")
        retrieval_system = ImageRetrievalSystem(
            index_path=INDEX_PATH,
            metadata_path=METADATA_PATH,
            nprobe=10,
            use_gpu=False
        )
    return retrieval_system


@router.post("/search")
async def search_image(file: UploadFile = File(...), k: int = 5):
    os.makedirs("tmp", exist_ok=True)
    temp_path = f"tmp/{uuid.uuid4()}_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        system = get_system()
        results = system.search(temp_path, k=k)

        return {
            "results": [
                {
                    "image": path,
                    "distance": dist,
                    "similarity": round(1 / (1 + dist), 4)
                }
                for path, dist in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)
