import json
import random

INPUT_FILE = "products3.json"
OUTPUT_FILE = "products_shuffled.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

random.shuffle(data)  # shuffle in place

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ JSON shuffled successfully")
