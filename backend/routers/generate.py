# from fastapi import APIRouter, UploadFile, File, Form, HTTPException
# from fastapi.responses import FileResponse
# import os
# from pathlib import Path
# import aiofiles
# from services import ai_engine
# import logging

# # Get backend directory
# BACKEND_DIR = Path(__file__).parent.parent
# DATASETS_DIR = BACKEND_DIR / "datasets"
# OUTPUTS_DIR = BACKEND_DIR / "outputs"

# logger = logging.getLogger(__name__)

# router = APIRouter(prefix="/generate", tags=["Generate"])


# @router.post("/")
# async def generate_meme(
#     prompt: str = Form(...),
#     logo: UploadFile = File(None)
# ):
#     """
#     Generate a meme with AI-generated image and caption
    
#     Args:
#         prompt: Text description for the meme
#         logo: Optional logo file to overlay on the meme
#     """
#     try:
#         logo_path = None
        
#         # Save logo if provided
#         if logo:
#             logos_dir = DATASETS_DIR / "logos"
#             logos_dir.mkdir(parents=True, exist_ok=True)
#             logo_path = str(logos_dir / logo.filename)
#             async with aiofiles.open(logo_path, 'wb') as f:
#                 content = await logo.read()
#                 await f.write(content)
        
#         # Generate meme
#         result_path = await ai_engine.create_meme(prompt, logo_path)
        
#         # Return relative path for frontend
#         return {
#             "image_path": result_path,
#             "image_url": f"/outputs/" + os.path.basename(result_path),
#             "prompt": prompt,
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error generating meme: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/download/{filename}")
# async def download_meme(filename: str):
#     """Download a generated meme by filename"""
#     file_path = OUTPUTS_DIR / filename
#     if not file_path.exists():
#         raise HTTPException(status_code=404, detail="File not found")
#     return FileResponse(str(file_path), media_type="image/png")

"""
File: backend/routers/generate.py
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Optional
import logging

from services.ai_engine import get_ai_engine
from services.trend_intelligence import get_trend_intelligence
from services.brand_memory import get_brand_memory
from services.analytics import get_analytics_service
from services.guardrails import get_guardrails_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generate", tags=["generation"])

BACKEND_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = BACKEND_DIR / "outputs"


@router.post("/")
async def generate_meme(
    prompt: str = Form(...),
    logo: Optional[UploadFile] = File(None),
    use_trends: bool = Form(False),
    brand_name: Optional[str] = Form(None),
    tone: Optional[str] = Form(None),
    voice: Optional[str] = Form(None)
):
    """Generate a meme with full AI pipeline."""
    try:
        ai_engine = get_ai_engine()
        trend_intel = get_trend_intelligence()
        brand_memory = get_brand_memory()
        analytics = get_analytics_service()
        guardrails = get_guardrails_service()

        trends = None
        if use_trends:
            trending_topics = trend_intel.get_trending_topics(limit=10)
            trends = [t["keyword"] for t in trending_topics[:5]]
            logger.info(f"Using trends: {trends}")

        if logo:
            logo_bytes = await logo.read()
            logo_path = brand_memory.save_logo(logo_bytes, logo.filename)
            brand_memory.update_brand(
                brand_name=brand_name,
                logo_path=logo_path,
                tone=tone,
                voice=voice
            )

        brand_context = brand_memory.get_brand_context()

        is_safe, safety_check = guardrails.check_content_safety(prompt)
        if not is_safe:
            raise HTTPException(status_code=400, detail={"issues": safety_check["issues"]})

        result = ai_engine.generate_meme(
            user_prompt=prompt,
            trends=trends,
            brand_context=brand_context
        )

        caption = result["caption"]
        image_desc = result["image_description"]
        safety_report = guardrails.get_safety_report(caption, image_desc)

        if not safety_report["overall_safe"]:
            result["safety_warning"] = "Content flagged for review"
            result["safety_report"] = safety_report

        event_id = analytics.log_generation(
            prompt=prompt,
            output_path=result["path"],
            caption=caption,
            metadata=result.get("metadata", {})
        )

        result["event_id"] = event_id
        brand_memory.add_caption_to_history(caption)
        result["recommended_hashtags"] = brand_memory.get_recommended_hashtags(caption)

        logger.info(f"Meme generated successfully: {result['filename']}")

        result["image_url"] = f"/outputs/{result['filename']}"
        result["download_url"] = f"/generate/download/{result['filename']}"

        return {"success": True, **result}

    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_meme(filename: str):
    """Download generated meme."""
    file_path = OUTPUTS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    analytics = get_analytics_service()
    for log in analytics.logs:
        if filename in log.get("output_path", ""):
            analytics.log_engagement(log["event_id"], "downloads")
            break

    return FileResponse(file_path, media_type="image/png", filename=filename)


@router.post("/rate/{event_id}")
async def rate_meme(event_id: str, rating: float):
    """Rate a generated meme (1–5 stars)."""
    if not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    analytics = get_analytics_service()
    analytics.log_rating(event_id, rating)
    return {"success": True, "message": "Rating recorded", "event_id": event_id}


@router.get("/history")
async def get_meme_history(limit: int = 50, skip: int = 0):
    """
    Get all generated memes from MongoDB
    
    Args:
        limit: Number of results per page (default 50)
        skip: Number of records to skip for pagination (default 0)
    """
    analytics = get_analytics_service()
    memes = analytics.get_all_memes_from_db(limit=limit, skip=skip)
    
    return {
        "success": True,
        "count": len(memes),
        "memes": memes,
        "pagination": {
            "limit": limit,
            "skip": skip
        }
    }


@router.get("/meme/{event_id}")
async def get_meme_details(event_id: str):
    """
    Get single meme details from MongoDB by event_id
    
    Args:
        event_id: Event ID (e.g., gen_20251116_011526_32)
    """
    analytics = get_analytics_service()
    meme = analytics.get_meme_by_id(event_id)
    
    if meme:
        return {"success": True, "meme": meme}
    
    raise HTTPException(status_code=404, detail=f"Meme not found: {event_id}")


@router.get("/top")
async def get_top_memes(limit: int = 10, metric: str = "likes"):
    """
    Get top performing memes from MongoDB
    
    Args:
        limit: Number of results (default 10)
        metric: Sort by metric (likes, shares, views, downloads)
    """
    valid_metrics = ["likes", "shares", "views", "downloads"]
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid metric. Choose from: {valid_metrics}"
        )
    
    analytics = get_analytics_service()
    memes = analytics.get_top_memes_from_db(limit=limit, metric=metric)
    
    return {
        "success": True,
        "metric": metric,
        "count": len(memes),
        "memes": memes
    }


@router.get("/rated")
async def get_highly_rated_memes(min_rating: float = 4.0, limit: int = 20):
    """
    Get highly rated memes from MongoDB
    
    Args:
        min_rating: Minimum rating (1-5, default 4.0)
        limit: Number of results (default 20)
    """
    if not (1 <= min_rating <= 5):
        raise HTTPException(status_code=400, detail="min_rating must be between 1 and 5")
    
    analytics = get_analytics_service()
    memes = analytics.get_memes_by_rating(min_rating=min_rating, limit=limit)
    
    return {
        "success": True,
        "min_rating": min_rating,
        "count": len(memes),
        "memes": memes
    }


@router.get("/stats/mongodb")
async def get_mongodb_stats():
    """
    Get MongoDB statistics and connection status
    """
    analytics = get_analytics_service()
    stats = analytics.get_mongodb_stats()
    
    return {"success": True, "stats": stats}

