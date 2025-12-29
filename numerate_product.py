import json

INPUT_FILE = "products_shuffled.json"
OUTPUT_FILE = "products_renumbered.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Renumber IDs from 1 to N
for index, item in enumerate(data, start=1):
    item["id"] = index

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ IDs renumbered from 1 to {len(data)}")
