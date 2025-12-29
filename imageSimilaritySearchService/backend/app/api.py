from fastapi import APIRouter, UploadFile, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import uuid
import math
import json
from sqlalchemy import create_engine, text

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

        enriched_results = []
        # here i load the metadata
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            METADATA = json.load(f)
        
        for path, dist in results:
            # searching for the product by its url
            meta = next(
                (v for v in METADATA.values() if v["path"] == path or v["filename"] in path),
                {}
            )
            enriched_results.append({
                "image": path,
                "distance": dist,
                "similarity": round(1 / (1 + dist), 4),
                "product_id": meta.get("product_id", "N/A"),
                "title": meta.get("title", "N/A")
            })

        return {"results": enriched_results}
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


@router.post("/index/postgres")
async def index_from_postgres(limit: int = 0, offset: int = 0):
    """Index images by reading products from Postgres (ecomApp_product).

    If `limit` is 0 (default) all products with a non-empty `image` will be indexed.
    """
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:fashionista20@postgres:5432/fashionista")
    engine = create_engine(db_url)

    os.makedirs("/tmp", exist_ok=True)
    json_path = f"/tmp/{uuid.uuid4()}.json"

    try:
        with engine.connect() as conn:
            # fetch products that have an image URL
            if limit and limit > 0:
                rows = conn.execute(
                    text('SELECT id, title, description, image '
                        'FROM "ecomApp_product" '
                        'WHERE image IS NOT NULL AND TRIM(image) <> :empty '
                        'ORDER BY id LIMIT :limit OFFSET :offset'),
                    {"empty": "", "limit": limit, "offset": offset}
                ).fetchall()
            else:
                rows = conn.execute(
                    text('SELECT id, title, description, image '
                        'FROM "ecomApp_product" '
                        'WHERE image IS NOT NULL AND TRIM(image) <> :empty '
                        'ORDER BY id OFFSET :offset'),
                    {"empty": "", "offset": offset}
                ).fetchall()


            # Build JSON payload expected by index_images_from_json
            entries = []
            for r in rows:
                r_dict = dict(r._mapping)
                entries.append({
                    "id": r_dict.get("id"),
                    "title": r_dict.get("title"),
                    "description": r_dict.get("description"),
                    "image": r_dict.get("image")
                })

        num_images = len(entries)

        if num_images == 0:
            raise HTTPException(status_code=400, detail="No images found in Postgres (no `image` URL)")

        # write temp json file and reuse existing JSON indexer
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f)

        n_regions = calculate_optimal_regions(num_images)
        nprobe = max(1, n_regions // 4)

        system = ImageRetrievalSystem(
            n_regions=n_regions,
            nprobe=nprobe,
            use_gpu=False
        )

        # Index from the temporary JSON file
        system.index_images_from_json(json_path=json_path)
        system.save(INDEX_PATH, METADATA_PATH)

        return {
            "status": "success",
            "indexed_images": num_images,
            "n_regions": n_regions,
            "nprobe": nprobe
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            os.remove(json_path)
        except Exception:
            pass
