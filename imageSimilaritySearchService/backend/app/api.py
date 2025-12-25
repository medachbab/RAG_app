from fastapi import APIRouter, UploadFile, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import uuid
import math
import json

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

def calculate_optimal_regions(num_images: int) -> int:
    #the common rule of choosing the optimal regions:
    if num_images < 100:
        return max(1, int(math.sqrt(num_images)))
    else:
        return min(int(4 * math.sqrt(num_images)), num_images // 2)


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

@router.post("/index/images")
async def index_images(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No images provided")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    image_paths = []

    try:
        for file in files:
            path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(path)

        num_images = len(image_paths)

        n_regions = calculate_optimal_regions(num_images)
        nprobe = max(1, n_regions // 4)

        system = ImageRetrievalSystem(
            n_regions=n_regions,
            nprobe=nprobe,
            use_gpu=False
        )

        system.index_images(image_dir=UPLOAD_DIR)
        system.save(INDEX_PATH, METADATA_PATH)

        reset_system()

        return {
            "status": "success",
            "indexed_images": num_images,
            "n_regions": n_regions,
            "nprobe": nprobe
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)



@router.post("/index/json")
async def index_from_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")

    os.makedirs("/tmp", exist_ok=True)
    json_path = f"/tmp/{uuid.uuid4()}.json"

    try:
        with open(json_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            num_images = len(data)
        elif isinstance(data, dict):
            num_images = len(data.get("products") or data.get("items") or [])
        else:
            num_images = 0

        if num_images == 0:
            raise ValueError("No images found in JSON")

        n_regions = calculate_optimal_regions(num_images)
        nprobe = max(1, n_regions // 4)

        system = ImageRetrievalSystem(
            n_regions=n_regions,
            nprobe=nprobe,
            use_gpu=False
        )

        system.index_images_from_json(json_path=json_path)
        system.save(INDEX_PATH, METADATA_PATH)

        reset_system()

        return {
            "status": "success",
            "indexed_images": num_images,
            "n_regions": n_regions,
            "nprobe": nprobe
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.remove(json_path)


