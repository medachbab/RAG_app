from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Image Similarity Search API")

allowed_origins = os.getenv("Search_FRONTEND_URL", "http://159.89.9.71:5174,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
