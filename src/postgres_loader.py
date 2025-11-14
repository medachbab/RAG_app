from sqlalchemy import create_engine, text
from langchain_core.documents import Document
from typing import List, Dict
import os

def load_products_from_postgres(batch_size=500) -> List[Dict]:
    """
    Fetch all products from PostgreSQL and return a list of documents suitable for RAG indexing.
    """
    db_url = os.environ.get("DATABASE_URL", "postgresql://rag_user:rag_pass@localhost:5432/ragdb")
    engine = create_engine(db_url)

    docs = []

    with engine.connect() as conn:
        offset = 0
        while True:
            query = text("""
                SELECT id, product_name, brand, category, material, fit_type, sizes_available, color,
                       description, user_reviews, washing_instructions, price, shipping_info, stock_status
                FROM products
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """)
            rows = conn.execute(query, {"limit": batch_size, "offset": offset}).fetchall()
            if not rows:
                break

            for r in rows:
                r_dict = dict(r._mapping)
                text_block = (
                    f"Product Name: {r_dict['product_name']}\n"
                    f"Brand: {r_dict['brand']}\n"
                    f"Category: {r_dict['category']}\n"
                    f"Material: {r_dict['material']}\n"
                    f"Fit: {r_dict['fit_type']}\n"
                    f"Available Sizes: {r_dict['sizes_available']}\n"
                    f"Color: {r_dict['color']}\n"
                    f"Description: {r_dict['description']}\n"
                    f"User Reviews: {r_dict['user_reviews']}\n"
                    f"Washing Instructions: {r_dict['washing_instructions']}\n"
                    f"Price: {r_dict['price']}\n"
                    f"Shipping Info: {r_dict['shipping_info']}\n"
                    f"Stock Status: {r_dict['stock_status']}"
                )
                docs.append(Document(page_content=text_block, metadata={"id": f"product_{r_dict['id']}"}))


            offset += len(rows)

    return docs
