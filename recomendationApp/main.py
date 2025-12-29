from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommender import recommend_products_service

app = FastAPI(title="Recommendation Microservice")

# Allow frontend (React) to call this API
origins = [
    "http://localhost:5173",  
    "http://164.92.170.172:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class RecommendationRequest(BaseModel):
    query: str

# POST /recommend endpoint
@app.post("/recommend")
def recommend(request: RecommendationRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is missing")
    recommended_products = recommend_products_service(request.query)
    return {"recommended_products": recommended_products}

# Optional: health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
