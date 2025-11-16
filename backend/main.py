from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from routers import generate, trends, brand, auth
from db.mongo import connect_to_mongo, close_mongo_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Request logging middleware
class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"📥 {request.method} {request.url.path} from {request.client.host}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(f"📤 {request.method} {request.url.path} -> {response.status_code} ({process_time:.2f}s)")
        
        return response

# Get backend directory
BACKEND_DIR = Path(__file__).parent
OUTPUTS_DIR = BACKEND_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="AI Meme & Marketing Generator", version="1.0.0")

# Add request logging middleware
app.add_middleware(RequestLoggerMiddleware)

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000,https://ai-memeforge.vercel.app"
).split(",")

logger.info(f"🔓 CORS enabled for origins: {ALLOWED_ORIGINS}")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount static files for serving generated images
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")

# Database lifecycle


@app.on_event("startup")
async def startup_event() -> None:
    try:
        logger.info("🚀 Starting AI MemeForge API...")
        await connect_to_mongo()
        logger.info("✅ Startup complete!")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event() -> None:
    try:
        logger.info("👋 Shutting down gracefully...")
        await close_mongo_connection()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Include routers
app.include_router(auth.router)
app.include_router(generate.router)
app.include_router(trends.router)
app.include_router(brand.router)


@app.get("/")
def home():
    return {
        "message": "AI MemeForge API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "generate": "/generate/",
            "trends": "/trends/",
            "brand": "/brand/",
            "auth": "/auth/"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI MemeForge API",
        "version": "1.0.0"
    }

