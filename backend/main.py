from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from routers import generate, trends, brand, auth
from db.mongo import connect_to_mongo, close_mongo_connection

# Get backend directory
BACKEND_DIR = Path(__file__).parent
OUTPUTS_DIR = BACKEND_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="AI Meme & Marketing Generator", version="1.0.0")

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000"
).split(",")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated images
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")

# Database lifecycle


@app.on_event("startup")
async def startup_event() -> None:
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_mongo_connection()


# Include routers
app.include_router(auth.router)
app.include_router(generate.router)
app.include_router(trends.router)
app.include_router(brand.router)


@app.get("/")
def home():
    return {"message": "AI MemeForge API is running!", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

