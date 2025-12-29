import json
import re

INPUT_FILE = "products_renumbered.json"
OUTPUT_FILE = "products_prices_normalized.json"

def normalize_price(price):
    if price is None:
        return None

    # Convert to string
    price_str = str(price)

    # Remove spaces
    price_str = price_str.replace(" ", "")

    # If format like "1,371.66" → remove thousand separator
    if re.match(r"^\d{1,3}(,\d{3})+\.\d+$", price_str):
        price_str = price_str.replace(",", "")

    # If format like "512,85" → decimal comma
    elif re.match(r"^\d+,\d+$", price_str):
        price_str = price_str.replace(",", ".")

    # Convert to float and force 2 decimals
    try:
        value = float(price_str)
        return f"{value:.2f}"
    except ValueError:
        return price  # fallback if something unexpected appears

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    item["price"] = normalize_price(item.get("price"))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Prices normalized to xx.xx format")
