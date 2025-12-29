import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_amazon_product(url, product_id):
    # Headers are essential to avoid being blocked by Amazon
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, "html.parser")

        # 1. Title
        title = soup.find("span", {"id": "productTitle"})
        title = title.get_text(strip=True) if title else "N/A"

        # 2. Price
        price_whole = soup.find("span", {"class": "a-price-whole"})
        price_fraction = soup.find("span", {"class": "a-price-fraction"})
        price = f"{price_whole.text}{price_fraction.text}" if price_whole else "0.00"

        # 3. Rating
        rating = soup.select_one("i.a-star-5 span.a-icon-alt")
        if not rating:
            rating = soup.find("span", {"class": "a-icon-alt"})
        rating_val = rating.text.split(" ")[0] if rating else "0.0"

        # 4. Description (Feature Bullets)
        desc_div = soup.find("div", {"id": "feature-bullets"})
        description = desc_div.get_text(separator=" ", strip=True) if desc_div else "N/A"

        # 5. Stock Status
        availability = soup.find("div", {"id": "availability"})
        stock = "Available" if availability and "In Stock" in availability.text else "Out of Stock"

        # 6. Image
        img_tag = soup.find("img", {"id": "landingImage"})
        image_url = img_tag['src'] if img_tag else ""

        # 7. Reviews (Top 3 approximations)
        reviews = []
        review_elements = soup.select(".review-text-content span")[:3]
        reviewer_names = soup.select(".a-profile-name")[:3]
        
        for i, rev in enumerate(review_elements):
            reviews.append({
                "id": 20000 + i, # Placeholder ID
                "product": product_id,
                "rating": 5, # Approximate
                "comment": rev.get_text(strip=True),
                "date": "2024-01-01T00:00:00Z",
                "reviewerName": reviewer_names[i].text if i < len(reviewer_names) else f"User_{i}"
            })

        return {
            "id": product_id,
            "title": title,
            "description": description,
            "category": "men jackets",
            "price": price,
            "rating": rating_val,
            "stock": stock,
            "image": image_url,
            "reviews": reviews
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Example Usage
product_url = "https://m.media-amazon.com/images/I/711Vy37a+SL._AC_UL320_.jpg" # Replace with your product URL
data = scrape_amazon_product(product_url, 498)

if data:
    print(json.dumps(data, indent=4))