from sqlalchemy import create_engine, text
from langchain_core.documents import Document
from typing import List
import os

def load_products_from_postgres(batch_size=500) -> List[Document]:

    db_url = os.environ.get("DATABASE_URL", "postgresql://rag_user:rag_pass@postgres:5432/ragdb")
    engine = create_engine(db_url)

    docs = []
    query_str = """
        SELECT 
            p.id, 
            p.title, 
            p.description, 
            p.price, 
            p.rating as avg_rating, 
            p.stock, 
            c.name as category_name,
            STRING_AGG(r.comment, ' | ') as reviews
        FROM "ecomApp_product" p
        LEFT JOIN "ecomApp_category" c ON p.category_id = c.id
        LEFT JOIN "ecomApp_review" r ON p.id = r.product_id
        GROUP BY p.id, c.name
        ORDER BY p.id
        LIMIT :limit OFFSET :offset
    """

    with engine.connect() as conn:
        offset = 0
        while True:
            rows = conn.execute(text(query_str), {"limit": batch_size, "offset": offset}).fetchall()
            if not rows:
                break

            for r in rows:
                r_dict = dict(r._mapping)
                
                # Constructing the RAG content block
                text_block = (
                    f"Product: {r_dict['title']}\n"
                    f"Category: {r_dict['category_name']}\n"
                    f"Price: ${r_dict['price']}\n"
                    f"Average Rating: {r_dict['avg_rating']}/5\n"
                    f"Stock Status: {r_dict['stock']}\n"
                    f"Description: {r_dict['description']}\n"
                    f"User Reviews: {r_dict['reviews'] if r_dict['reviews'] else 'No reviews yet.'}"
                )
                
                docs.append(
                    Document(
                        page_content=text_block, 
                        metadata={
                            "id": r_dict['id'],
                            "source": "postgres_db",
                            "category": r_dict['category_name']
                        }
                    )
                )

            offset += len(rows)

    return docs