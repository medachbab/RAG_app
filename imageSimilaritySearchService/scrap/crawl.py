import requests
from bs4 import BeautifulSoup
import json
import time
import random

def scrape_amazon_mens_clothing(num_pages=1):
    all_products = []
    base_url = "https://www.amazon.com/s?k=amazon+puffer+jacket&adgrpid=82197443235&hvadid=673440924121&hvdev=c&hvlocphy=1029448&hvnetw=g&hvqmt=e&hvrand=157292365561366005&hvtargid=kwd-344620921422&hydadcr=22363_13507821&mcid=55dd5a47bc1a396b99d86b1f05105a57"
    
    # Realistic headers are CRITICAL to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    for page in range(1, num_pages + 1):
        print(f"Scraping Page {page}...")
        url = f"{base_url}{page}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find all product containers
            products = soup.find_all("div", {"data-component-type": "s-search-result"})

            for product in products:
                try:
                    # Extract ID (ASIN)
                    p_id = product.get("data-asin")
                    
                    # Extract Title
                    title_tag = product.find("h2", {"class": "a-size-mini"})
                    title = title_tag.text.strip() if title_tag else "N/A"

                    # Extract Price
                    price_whole = product.find("span", {"class": "a-price-whole"})
                    price_fraction = product.find("span", {"class": "a-price-fraction"})
                    price = f"{price_whole.text.strip()}{price_fraction.text.strip()}" if price_whole and price_fraction else "0.00"

                    # Extract Rating
                    rating_tag = product.find("span", {"class": "a-icon-alt"})
                    rating = rating_tag.text.split(" ")[0] if rating_tag else "0.0"

                    # Extract Image URL
                    image_tag = product.find("img", {"class": "s-image"})
                    image_url = image_tag.get("src") if image_tag else ""

                    # Construct JSON object matching your format
                    item = {
                        "id": p_id,
                        "title": title,
                        "description": f"Men's clothing item: {title}",
                        "category": "Mens cloths",
                        "price": price,
                        "rating": rating,
                        "stock": "Available",
                        "image": image_url,
                        "reviews": []
                    }
                    all_products.append(item)
                    
                except Exception as e:
                    continue

            # Random delay to mimic human behavior and avoid bans
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"Error on page {page}: {e}")

    # Save to JSON file
    with open("amazon_mens_cloths.json", "w") as f:
        json.dump(all_products, f, indent=4)
    
    print(f"Successfully scraped {len(all_products)} items.")

if __name__ == "__main__":
    scrape_amazon_mens_clothing(4)