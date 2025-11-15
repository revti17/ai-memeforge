"""
Trend Intelligence Service
Collects and normalizes trend data from multiple sources
"""

import requests
import logging
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory setup
BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"
TRENDS_CACHE_FILE = DATASETS_DIR / "trends_cache.json"


class TrendIntelligence:
    """
    Multi-source trend aggregation and normalization
    Sources: Google Trends, Reddit (via API), Twitter-like patterns
    """
    
    def __init__(self):
        self.cache_duration = 3600  # 1 hour cache
        self.trends_cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cached trends"""
        if TRENDS_CACHE_FILE.exists():
            try:
                with open(TRENDS_CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    # Check if cache is still valid
                    if cache.get("timestamp"):
                        cache_time = datetime.fromisoformat(cache["timestamp"])
                        if datetime.now() - cache_time < timedelta(seconds=self.cache_duration):
                            logger.info("Using cached trends")
                            return cache
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        
        return {"trends": [], "timestamp": None}
    
    def _save_cache(self, trends: List[Dict]):
        """Save trends to cache"""
        try:
            DATASETS_DIR.mkdir(exist_ok=True)
            cache_data = {
                "trends": trends,
                "timestamp": datetime.now().isoformat(),
                "sources": ["google_trends", "reddit", "synthetic"]
            }
            with open(TRENDS_CACHE_FILE, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logger.info(f"Cached {len(trends)} trends")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def fetch_google_trends(self, geo: str = "US", category: int = 0) -> List[Dict]:
        """
        Fetch trending searches from Google Trends
        
        Args:
            geo: Country code (e.g., 'US', 'GB', 'IN')
            category: Category ID (0 = all categories)
            
        Returns:
            List of trend dictionaries
        """
        trends = []
        
        try:
            # Google Trends Daily API endpoint
            url = f"https://trends.google.com/trends/api/dailytrends"
            params = {
                "hl": "en-US",
                "tz": -300,
                "geo": geo,
                "ns": 15
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Remove )]}' prefix that Google adds
                json_text = response.text.replace(")]}'", "", 1)
                data = json.loads(json_text)
                
                # Parse trending searches
                if "default" in data and "trendingSearchesDays" in data["default"]:
                    for day in data["default"]["trendingSearchesDays"][:1]:  # Today only
                        for item in day.get("trendingSearches", [])[:20]:
                            query = item.get("title", {}).get("query", "")
                            traffic = item.get("formattedTraffic", "0")
                            
                            if query:
                                trends.append({
                                    "keyword": query,
                                    "source": "google_trends",
                                    "score": self._parse_traffic(traffic),
                                    "category": "general",
                                    "timestamp": datetime.now().isoformat()
                                })
                
                logger.info(f"Fetched {len(trends)} trends from Google Trends")
                
        except Exception as e:
            logger.warning(f"Google Trends fetch failed: {e}")
        
        return trends
    
    def fetch_reddit_trends(self, subreddits: List[str] = None) -> List[Dict]:
        """
        Fetch trending topics from Reddit
        Uses Reddit's public JSON endpoints (no auth required)
        
        Args:
            subreddits: List of subreddit names to check
            
        Returns:
            List of trend dictionaries
        """
        if subreddits is None:
            subreddits = ["all", "memes", "dankmemes", "me_irl", "wholesomememes"]
        
        trends = []
        
        for subreddit in subreddits[:5]:  # Limit to 5 to avoid rate limits
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {"User-Agent": "AIMemeForge/1.0"}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    for post in posts[:10]:  # Top 10 hot posts
                        post_data = post.get("data", {})
                        title = post_data.get("title", "")
                        score = post_data.get("score", 0)
                        
                        # Extract keywords from title
                        keywords = self._extract_keywords(title)
                        
                        for keyword in keywords:
                            trends.append({
                                "keyword": keyword,
                                "source": f"reddit_{subreddit}",
                                "score": score,
                                "category": "social",
                                "timestamp": datetime.now().isoformat()
                            })
                
                # Respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"Reddit fetch failed for r/{subreddit}: {e}")
        
        logger.info(f"Fetched {len(trends)} trends from Reddit")
        return trends
    
    def _parse_traffic(self, traffic_str: str) -> float:
        """Parse traffic string (e.g., '500K+', '1M+') to numeric score"""
        try:
            traffic_str = traffic_str.replace('+', '').replace(',', '').upper()
            
            if 'M' in traffic_str:
                return float(traffic_str.replace('M', '')) * 1000000
            elif 'K' in traffic_str:
                return float(traffic_str.replace('K', '')) * 1000
            else:
                return float(traffic_str)
        except:
            return 0.0
    
    def _extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|@\w+|#\w+', '', text)
        
        # Split and clean
        words = text.lower().split()
        
        # Filter stop words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'this', 
                      'that', 'it', 'not', 'will', 'can', 'has', 'have', 'had'}
        
        keywords = [
            word.strip('.,!?;:()[]{}') 
            for word in words 
            if len(word) >= min_length and word not in stop_words
        ]
        
        return keywords[:5]  # Return top 5 keywords
    
    def normalize_trends(self, trends: List[Dict]) -> List[Dict]:
        """
        Normalize and deduplicate trends from multiple sources
        
        Args:
            trends: Raw trends from different sources
            
        Returns:
            Normalized and ranked trends
        """
        # Aggregate by keyword
        keyword_data = {}
        
        for trend in trends:
            keyword = trend["keyword"].lower()
            
            if keyword not in keyword_data:
                keyword_data[keyword] = {
                    "keyword": trend["keyword"],  # Keep original casing
                    "sources": [],
                    "total_score": 0,
                    "categories": set(),
                    "first_seen": trend.get("timestamp")
                }
            
            keyword_data[keyword]["sources"].append(trend["source"])
            keyword_data[keyword]["total_score"] += trend["score"]
            keyword_data[keyword]["categories"].add(trend.get("category", "general"))
        
        # Convert to list and add metrics
        normalized = []
        for keyword, data in keyword_data.items():
            normalized.append({
                "keyword": data["keyword"],
                "score": data["total_score"],
                "source_count": len(set(data["sources"])),
                "sources": list(set(data["sources"])),
                "categories": list(data["categories"]),
                "velocity": data["total_score"] / max(len(data["sources"]), 1),  # Score per source
                "timestamp": data["first_seen"]
            })
        
        # Sort by score (descending)
        normalized.sort(key=lambda x: x["score"], reverse=True)
        
        return normalized
    
    def get_trending_topics(
        self, 
        limit: int = 20,
        min_score: float = 100,
        categories: Optional[List[str]] = None,
        force_refresh: bool = False
    ) -> List[Dict]:
        """
        Get aggregated trending topics from all sources
        
        Args:
            limit: Maximum number of trends to return
            min_score: Minimum score threshold
            categories: Filter by categories
            force_refresh: Force refresh even if cache is valid
            
        Returns:
            List of top trending topics
        """
        # Check cache first
        if not force_refresh and self.trends_cache.get("trends"):
            logger.info("Returning cached trends")
            cached_trends = self.trends_cache["trends"]
            
            # Apply filters
            filtered = self._apply_filters(cached_trends, min_score, categories)
            return filtered[:limit]
        
        # Fetch from all sources
        logger.info("Fetching fresh trends from all sources...")
        
        all_trends = []
        
        # Google Trends
        google_trends = self.fetch_google_trends()
        all_trends.extend(google_trends)
        
        # Reddit
        reddit_trends = self.fetch_reddit_trends()
        all_trends.extend(reddit_trends)
        
        # Normalize and deduplicate
        normalized_trends = self.normalize_trends(all_trends)
        
        # Save to cache
        self._save_cache(normalized_trends)
        self.trends_cache = {"trends": normalized_trends, "timestamp": datetime.now().isoformat()}
        
        # Apply filters
        filtered = self._apply_filters(normalized_trends, min_score, categories)
        
        return filtered[:limit]
    
    def _apply_filters(
        self, 
        trends: List[Dict], 
        min_score: float, 
        categories: Optional[List[str]]
    ) -> List[Dict]:
        """Apply score and category filters"""
        filtered = trends
        
        # Score filter
        if min_score > 0:
            filtered = [t for t in filtered if t["score"] >= min_score]
        
        # Category filter
        if categories:
            filtered = [
                t for t in filtered 
                if any(cat in t.get("categories", []) for cat in categories)
            ]
        
        return filtered
    
    def get_trend_suggestions(self, user_input: str, top_k: int = 5) -> List[str]:
        """
        Get trend suggestions related to user input
        
        Args:
            user_input: User's meme prompt
            top_k: Number of suggestions
            
        Returns:
            List of related trending keywords
        """
        trends = self.get_trending_topics(limit=50)
        
        if not trends:
            return []
        
        # Extract keywords from user input
        user_keywords = set(self._extract_keywords(user_input))
        
        # Score trends by relevance to user input
        scored_trends = []
        for trend in trends:
            trend_keywords = set(self._extract_keywords(trend["keyword"]))
            
            # Calculate keyword overlap
            overlap = len(user_keywords & trend_keywords)
            relevance_score = overlap + (trend["score"] / 1000000)  # Combine overlap with trend score
            
            if relevance_score > 0:
                scored_trends.append({
                    "keyword": trend["keyword"],
                    "relevance": relevance_score
                })
        
        # Sort by relevance
        scored_trends.sort(key=lambda x: x["relevance"], reverse=True)
        
        return [t["keyword"] for t in scored_trends[:top_k]]
    
    def get_trending_hashtags(self, limit: int = 10) -> List[str]:
        """Generate trending hashtags from current trends"""
        trends = self.get_trending_topics(limit=limit)
        
        hashtags = []
        for trend in trends:
            # Convert to hashtag format
            keyword = trend["keyword"]
            # Remove spaces and special chars
            hashtag = "#" + "".join(c for c in keyword if c.isalnum())
            if len(hashtag) > 1:  # Must have at least one char after #
                hashtags.append(hashtag)
        
        return hashtags[:limit]


# Singleton instance
_trend_intelligence = None

def get_trend_intelligence() -> TrendIntelligence:
    """Get or create Trend Intelligence singleton"""
    global _trend_intelligence
    if _trend_intelligence is None:
        _trend_intelligence = TrendIntelligence()
    return _trend_intelligence