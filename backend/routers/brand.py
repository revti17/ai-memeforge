"""
File: backend/routers/brand.py
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
import logging

from services.brand_memory import get_brand_memory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/brand", tags=["brand"])


@router.post("/upload")
async def upload_brand(
    logo: UploadFile = File(...),
    brand_name: Optional[str] = Form(None),
    tone: Optional[str] = Form("humorous"),
    voice: Optional[str] = Form("casual"),
    target_audience: Optional[str] = Form("general"),
    hashtags: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None)
):
    """Upload brand logo and settings."""
    try:
        brand_memory = get_brand_memory()
        logo_bytes = await logo.read()
        logo_path = brand_memory.save_logo(logo_bytes, logo.filename)

        hashtags_list = json.loads(hashtags) if hashtags else []
        keywords_list = json.loads(keywords) if keywords else []

        brand_data = brand_memory.update_brand(
            brand_name=brand_name,
            logo_path=logo_path,
            tone=tone,
            voice=voice,
            target_audience=target_audience,
            hashtags=hashtags_list,
            keywords=keywords_list
        )

        return {"success": True, "message": "Brand updated successfully", "brand": brand_data}
    except Exception as e:
        logger.error(f"Brand upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_brand():
    """Get current brand settings."""
    try:
        brand_memory = get_brand_memory()
        return {"success": True, "brand": brand_memory.get_brand_context()}
    except Exception as e:
        logger.error(f"Failed to get brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_brand():
    """Export complete brand profile."""
    try:
        brand_memory = get_brand_memory()
        return {"success": True, "profile": brand_memory.export_brand_profile()}
    except Exception as e:
        logger.error(f"Failed to export brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import")
async def import_brand(profile: dict):
    """Import brand profile from JSON."""
    try:
        brand_memory = get_brand_memory()
        brand_memory.import_brand_profile(profile)
        return {"success": True, "message": "Brand profile imported successfully"}
    except Exception as e:
        logger.error(f"Failed to import brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_brand():
    """Reset brand to default settings."""
    try:
        brand_memory = get_brand_memory()
        brand_memory.reset_brand()
        return {"success": True, "message": "Brand reset to defaults"}
    except Exception as e:
        logger.error(f"Failed to reset brand: {e}")
        raise HTTPException(status_code=500, detail=str(e))
