# from fastapi import APIRouter, HTTPException
# import requests
# import logging

# logger = logging.getLogger(__name__)

# router = APIRouter(prefix="/trends", tags=["Trends"])


# @router.get("/")
# async def fetch_trends():
#     """
#     Fetch trending topics from Google Trends
#     Returns top 5 trending searches
#     """
#     try:
#         from pytrends.request import TrendReq
        
#         pytrends = TrendReq(hl='en-US', tz=360)
#         trending = pytrends.trending_searches(pn='united_states')
        
#         # Convert to list
#         trends_list = trending.head(10).values.flatten().tolist()
        
#         return {
#             "trending": trends_list[:10],
#             "count": len(trends_list)
#         }
#     except Exception as e:
#         logger.error(f"Error fetching trends: {e}")
#         # Fallback to sample trends if API fails
#         return {
#             "trending": [
#                 "AI memes",
#                 "Viral marketing",
#                 "Social media trends",
#                 "Digital content",
#                 "Creative marketing"
#             ],
#             "count": 5,
#             "note": "Using fallback data - Google Trends API unavailable"
#         }


# @router.get("/suggestions")
# async def get_suggestions(keyword: str = ""):
#     """
#     Get trend suggestions based on keyword
#     """
#     try:
#         from pytrends.request import TrendReq
        
#         pytrends = TrendReq(hl='en-US', tz=360)
#         suggestions = pytrends.suggestions(keyword)
        
#         return {
#             "keyword": keyword,
#             "suggestions": suggestions[:5] if suggestions else []
#         }
#     except Exception as e:
#         logger.error(f"Error getting suggestions: {e}")
#         return {
#             "keyword": keyword,
#             "suggestions": [],
#             "error": str(e)
#         }

"""
File: backend/routers/trends.py
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging
from services.trend_intelligence import get_trend_intelligence

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/trends", tags=["trends"])


@router.get("/")
async def get_trends(
    limit: int = Query(20, ge=1, le=100),
    min_score: float = Query(0, ge=0),
    category: Optional[str] = None,
    force_refresh: bool = False
):
    """Get trending topics from multiple sources."""
    try:
        trend_intel = get_trend_intelligence()
        categories = [category] if category else None
        trends = trend_intel.get_trending_topics(
            limit=limit, min_score=min_score, categories=categories, force_refresh=force_refresh
        )
        return {"success": True, "count": len(trends), "trends": trends}
    except Exception as e:
        logger.error(f"Failed to fetch trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
async def get_trend_suggestions(
    prompt: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20)
):
    """Get trend suggestions related to user prompt."""
    try:
        trend_intel = get_trend_intelligence()
        suggestions = trend_intel.get_trend_suggestions(prompt, top_k=top_k)
        return {"success": True, "prompt": prompt, "suggestions": suggestions}
    except Exception as e:
        logger.error(f"Failed to get suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hashtags")
async def get_trending_hashtags(limit: int = Query(10, ge=1, le=30)):
    """Get trending hashtags."""
    try:
        trend_intel = get_trend_intelligence()
        hashtags = trend_intel.get_trending_hashtags(limit=limit)
        return {"success": True, "count": len(hashtags), "hashtags": hashtags}
    except Exception as e:
        logger.error(f"Failed to get hashtags: {e}")
        raise HTTPException(status_code=500, detail=str(e))
