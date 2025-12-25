import json
from langchain_core.documents import Document
from typing import List

def load_products_from_json(file_path: str) -> List[Document]:
    """
    Reads product data from a JSON file and converts it into LangChain Documents.
    """
    docs = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            # Extract and format reviews into a single string
            reviews_list = item.get("reviews", [])
            formatted_reviews = " | ".join([
                f"{rev.get('reviewerName')}: {rev.get('comment')} ({rev.get('rating')} stars)" 
                for rev in reviews_list
            ])

            # Construct the text block for the vector store
            text_block = (
                f"Product Name: {item.get('title')}\n"
                f"Category: {item.get('category')}\n"
                f"Description: {item.get('description')}\n"
                f"Price: {item.get('price')}\n"
                f"Rating: {item.get('rating')}\n"
                f"Stock Status: {item.get('stock')}\n"
                f"Washing Instructions: {item.get('washing_instructions')}\n"
                f"Shipping Info: {item.get('shipping_info')}\n"
                f"User Reviews: {formatted_reviews}"
            )

            # Create the Document object
            docs.append(
                Document(
                    page_content=text_block, 
                    metadata={"id": f"json_product_{item.get('id')}"}
                )
            )

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return docs