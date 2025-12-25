import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

INDEX_PATH = os.path.join(DATA_DIR, "image_index.faiss")
METADATA_PATH = os.path.join(DATA_DIR, "image_metadata.json")
