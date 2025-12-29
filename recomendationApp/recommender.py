import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")

# Load dataset
products = pd.read_json(FILE_PATH)

# Prepare features
products["combined"] = products["category"] + " " + products["description"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_df=0.95,
    min_df=2
)

X = vectorizer.fit_transform(products["combined"])

kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(X)

products["cluster"] = kmeans.labels_

def recommend_products_service(query: str):
    vector = vectorizer.transform([query])
    similarities = cosine_similarity(vector, kmeans.cluster_centers_)
    cluster_id = np.argmax(similarities)

    recommended = products[products["cluster"] == cluster_id].head(4)

    return recommended[
        ["id", "title", "category", "price", "rating", "description", "image"]
    ].to_dict(orient="records")
