"""
Analytics Service with Feedback Loop
Logs events, tracks engagement, and provides learning signals for model improvement
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict, Counter
import statistics
from db.mongo_sync import get_database_sync
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory setup
BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"
LOGS_FILE = DATASETS_DIR / "analytics_logs.json"
ENGAGEMENT_FILE = DATASETS_DIR / "engagement_data.json"
LEARNING_SIGNALS_FILE = DATASETS_DIR / "learning_signals.json"


class AnalyticsService:
    """
    Comprehensive analytics and feedback loop system
    Tracks: generations, engagement, performance, learning signals
    Uses MongoDB for storage with JSON fallback
    """
    
    def __init__(self):
        DATASETS_DIR.mkdir(exist_ok=True)
        self.use_mongodb = True
        try:
            self.db = get_database_sync()
            self.memes_collection = self.db["meme_generations"]
            self.caption_patterns_collection = self.db["caption_patterns"]
            self.prompt_examples_collection = self.db["prompt_examples"]
            logger.info("✅ AnalyticsService initialized with MongoDB")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB not available, falling back to JSON: {e}")
            self.use_mongodb = False
        
        # Keep JSON as fallback
        self.logs = self._load_logs()
        self.engagement_data = self._load_engagement_data()
        self.learning_signals = self._load_learning_signals()
    
    def _load_logs(self) -> List[Dict]:
        """Load analytics logs"""
        if LOGS_FILE.exists():
            try:
                with open(LOGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load logs: {e}")
        return []
    
    def _save_logs(self):
        """Save analytics logs"""
        try:
            with open(LOGS_FILE, 'w') as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save logs: {e}")
    
    def _load_engagement_data(self) -> Dict:
        """Load engagement tracking data"""
        if ENGAGEMENT_FILE.exists():
            try:
                with open(ENGAGEMENT_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load engagement data: {e}")
        return {"memes": {}, "captions": {}}
    
    def _save_engagement_data(self):
        """Save engagement tracking data"""
        try:
            with open(ENGAGEMENT_FILE, 'w') as f:
                json.dump(self.engagement_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save engagement data: {e}")
    
    def _load_learning_signals(self) -> Dict:
        """Load learning signals for model improvement"""
        if LEARNING_SIGNALS_FILE.exists():
            try:
                with open(LEARNING_SIGNALS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load learning signals: {e}")
        return {
            "prompt_examples": [],
            "caption_patterns": [],
            "negative_examples": [],
            "last_updated": None
        }
    
    def _save_learning_signals(self):
        """Save learning signals"""
        try:
            self.learning_signals["last_updated"] = datetime.now().isoformat()
            with open(LEARNING_SIGNALS_FILE, 'w') as f:
                json.dump(self.learning_signals, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save learning signals: {e}")
    
    def log_generation(
        self,
        prompt: str,
        output_path: str,
        caption: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Log a meme generation event
        
        Args:
            prompt: User prompt
            output_path: Path to generated meme
            caption: Generated caption
            metadata: Additional metadata
            
        Returns:
            Event ID
        """
        import random
        event_id = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(10, 99)}"
        
        log_entry = {
            "event_id": event_id,
            "event_type": "generation",
            "timestamp": datetime.now(),
            "prompt": prompt,
            "enhanced_prompt": metadata.get("enhanced_prompt") if metadata else None,
            "output_path": output_path,
            "filename": Path(output_path).name,
            "caption": caption,
            "trends_used": metadata.get("trends_used", []) if metadata else [],
            "brand_settings": metadata.get("brand_settings") if metadata else None,
            "metadata": metadata or {},
            "engagement": {
                "views": 0,
                "likes": 0,
                "shares": 0,
                "downloads": 0,
                "rating": None
            }
        }
        
        # Save to MongoDB
        if self.use_mongodb:
            try:
                result = self.memes_collection.insert_one(log_entry.copy())
                logger.info(f"✅ Logged to MongoDB: {event_id} (ID: {result.inserted_id})")
            except Exception as e:
                logger.error(f"❌ MongoDB insert failed: {e}, falling back to JSON")
                self.use_mongodb = False
        
        # Always save to JSON as backup (convert datetime to string)
        log_entry_json = {
            "event_id": event_id,
            "event_type": "generation",
            "timestamp": log_entry["timestamp"].isoformat(),
            "prompt": prompt,
            "enhanced_prompt": metadata.get("enhanced_prompt") if metadata else None,
            "output_path": output_path,
            "filename": Path(output_path).name,
            "caption": caption,
            "trends_used": metadata.get("trends_used", []) if metadata else [],
            "brand_settings": metadata.get("brand_settings") if metadata else None,
            "metadata": metadata or {},
            "engagement": {
                "views": 0,
                "likes": 0,
                "shares": 0,
                "downloads": 0,
                "rating": None
            }
        }
        self.logs.append(log_entry_json)
        self._save_logs()
        
        # Initialize engagement tracking
        self.engagement_data["memes"][event_id] = log_entry["engagement"]
        self.engagement_data["captions"][caption] = {
            "uses": 1,
            "avg_engagement": 0,
            "event_ids": [event_id]
        }
        self._save_engagement_data()
        
        logger.info(f"Logged generation event: {event_id}")
        return event_id
    
    def log_engagement(
        self,
        event_id: str,
        engagement_type: str,
        value: int = 1
    ):
        """
        Log engagement event (view, like, share, download)
        
        Args:
            event_id: Generation event ID
            engagement_type: Type of engagement (views, likes, shares, downloads)
            value: Engagement value (default 1)
        """
        # Update MongoDB
        if self.use_mongodb:
            try:
                result = self.memes_collection.update_one(
                    {"event_id": event_id},
                    {"$inc": {f"engagement.{engagement_type}": value}}
                )
                if result.modified_count > 0:
                    logger.info(f"✅ Updated {engagement_type} in MongoDB for {event_id}")
            except Exception as e:
                logger.error(f"❌ MongoDB update failed: {e}")
        
        # Update JSON
        if event_id in self.engagement_data["memes"]:
            if engagement_type in self.engagement_data["memes"][event_id]:
                self.engagement_data["memes"][event_id][engagement_type] += value
                self._save_engagement_data()
                logger.info(f"Logged {engagement_type} for {event_id}")
            else:
                logger.warning(f"Unknown engagement type: {engagement_type}")
        else:
            logger.warning(f"Event ID not found: {event_id}")
    
    def log_rating(
        self,
        event_id: str,
        rating: float  # 1-5 stars
    ):
        """
        Log user rating for generated meme
        
        Args:
            event_id: Generation event ID
            rating: Rating value (1-5)
        """
        # Update MongoDB
        if self.use_mongodb:
            try:
                result = self.memes_collection.update_one(
                    {"event_id": event_id},
                    {"$set": {"engagement.rating": rating}}
                )
                if result.modified_count > 0:
                    logger.info(f"✅ Updated rating in MongoDB for {event_id}: {rating}/5")
            except Exception as e:
                logger.error(f"❌ MongoDB rating update failed: {e}")
        
        # Update JSON
        if event_id in self.engagement_data["memes"]:
            self.engagement_data["memes"][event_id]["rating"] = rating
            self._save_engagement_data()
            logger.info(f"Logged rating {rating} for {event_id}")
            
            # Add to learning signals
            self._update_learning_signals(event_id, rating)
        else:
            logger.warning(f"Event ID not found: {event_id}")
    
    def _update_learning_signals(self, event_id: str, rating: float):
        """
        Update learning signals based on user feedback
        
        Args:
            event_id: Generation event ID
            rating: User rating
        """
        # Find the log entry
        log_entry = next((log for log in self.logs if log["event_id"] == event_id), None)
        
        if not log_entry:
            return
        
        prompt = log_entry["prompt"]
        caption = log_entry["caption"]
        enhanced_prompt = log_entry.get("metadata", {}).get("enhanced_prompt", "")
        
        # Add to prompt examples if highly rated
        if rating >= 4.0:
            self.learning_signals["prompt_examples"].append({
                "user_input": prompt,
                "enhanced_prompt": enhanced_prompt or prompt,
                "rating": rating,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only top 50 examples
            self.learning_signals["prompt_examples"].sort(key=lambda x: x["rating"], reverse=True)
            self.learning_signals["prompt_examples"] = self.learning_signals["prompt_examples"][:50]
        
        # Add to caption patterns if highly rated
        if rating >= 4.0:
            self.learning_signals["caption_patterns"].append({
                "caption": caption,
                "prompt": prompt,
                "rating": rating,
                "engagement": self.engagement_data["memes"].get(event_id, {}),
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only top 50 patterns
            self.learning_signals["caption_patterns"].sort(key=lambda x: x["rating"], reverse=True)
            self.learning_signals["caption_patterns"] = self.learning_signals["caption_patterns"][:50]
        
        # Add to negative examples if poorly rated
        if rating <= 2.0:
            self.learning_signals["negative_examples"].append({
                "prompt": prompt,
                "caption": caption,
                "rating": rating,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 30 negative examples
            self.learning_signals["negative_examples"] = self.learning_signals["negative_examples"][-30:]
        
        self._save_learning_signals()
    
    def get_stats(self, days: int = 7) -> Dict:
        """
        Get analytics statistics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Statistics dictionary
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent logs
        recent_logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) >= cutoff_date
        ]
        
        if not recent_logs:
            return {
                "total_generations": 0,
                "period_days": days,
                "message": "No data for this period"
            }
        
        # Calculate statistics
        total_generations = len(recent_logs)
        
        # Engagement totals
        total_views = sum(
            self.engagement_data["memes"].get(log["event_id"], {}).get("views", 0)
            for log in recent_logs
        )
        total_likes = sum(
            self.engagement_data["memes"].get(log["event_id"], {}).get("likes", 0)
            for log in recent_logs
        )
        total_shares = sum(
            self.engagement_data["memes"].get(log["event_id"], {}).get("shares", 0)
            for log in recent_logs
        )
        total_downloads = sum(
            self.engagement_data["memes"].get(log["event_id"], {}).get("downloads", 0)
            for log in recent_logs
        )
        
        # Average engagement
        avg_views = total_views / total_generations if total_generations > 0 else 0
        avg_likes = total_likes / total_generations if total_generations > 0 else 0
        
        # Ratings
        ratings = [
            self.engagement_data["memes"].get(log["event_id"], {}).get("rating")
            for log in recent_logs
        ]
        ratings = [r for r in ratings if r is not None]
        
        avg_rating = statistics.mean(ratings) if ratings else None
        
        # Top prompts
        prompt_counter = Counter(log["prompt"] for log in recent_logs)
        top_prompts = prompt_counter.most_common(5)
        
        # Generation times
        generation_times = [
            log.get("metadata", {}).get("generation_time", 0)
            for log in recent_logs
        ]
        generation_times = [t for t in generation_times if t > 0]
        avg_generation_time = statistics.mean(generation_times) if generation_times else 0
        
        return {
            "period_days": days,
            "total_generations": total_generations,
            "engagement": {
                "total_views": total_views,
                "total_likes": total_likes,
                "total_shares": total_shares,
                "total_downloads": total_downloads,
                "avg_views_per_meme": round(avg_views, 2),
                "avg_likes_per_meme": round(avg_likes, 2),
                "engagement_rate": round((total_likes / total_views * 100) if total_views > 0 else 0, 2)
            },
            "ratings": {
                "total_ratings": len(ratings),
                "avg_rating": round(avg_rating, 2) if avg_rating else None
            },
            "performance": {
                "avg_generation_time": round(avg_generation_time, 2)
            },
            "top_prompts": [{"prompt": p, "count": c} for p, c in top_prompts],
            "trends": self._calculate_trends(recent_logs)
        }
    
    def _calculate_trends(self, logs: List[Dict]) -> Dict:
        """Calculate trend metrics"""
        if not logs:
            return {}
        
        # Group by day
        daily_counts = defaultdict(int)
        for log in logs:
            date = datetime.fromisoformat(log["timestamp"]).date().isoformat()
            daily_counts[date] += 1
        
        # Calculate growth
        sorted_days = sorted(daily_counts.items())
        if len(sorted_days) >= 2:
            recent_avg = statistics.mean([count for _, count in sorted_days[-3:]])
            older_avg = statistics.mean([count for _, count in sorted_days[:-3]]) if len(sorted_days) > 3 else sorted_days[0][1]
            growth_rate = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            growth_rate = 0
        
        return {
            "daily_generation_counts": dict(daily_counts),
            "growth_rate_percent": round(growth_rate, 2)
        }
    
    def get_learning_signals(self) -> Dict:
        """Get learning signals for model improvement"""
        return self.learning_signals
    
    def get_top_performing_memes(self, limit: int = 10, metric: str = "likes") -> List[Dict]:
        """
        Get top performing memes
        
        Args:
            limit: Number of results
            metric: Engagement metric to sort by (likes, shares, views)
            
        Returns:
            List of top performing meme data
        """
        # Score all memes
        scored_memes = []
        
        for log in self.logs:
            event_id = log["event_id"]
            engagement = self.engagement_data["memes"].get(event_id, {})
            
            score = engagement.get(metric, 0)
            
            scored_memes.append({
                "event_id": event_id,
                "prompt": log["prompt"],
                "caption": log["caption"],
                "output_path": log["output_path"],
                "timestamp": log["timestamp"],
                "engagement": engagement,
                "score": score
            })
        
        # Sort by score
        scored_memes.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_memes[:limit]
    
    def get_caption_performance(self, caption: str) -> Dict:
        """
        Get performance data for a specific caption
        
        Args:
            caption: Caption text
            
        Returns:
            Performance dictionary
        """
        if caption in self.engagement_data["captions"]:
            caption_data = self.engagement_data["captions"][caption]
            
            # Calculate average engagement across all uses
            event_ids = caption_data.get("event_ids", [])
            engagements = [
                self.engagement_data["memes"].get(eid, {})
                for eid in event_ids
            ]
            
            avg_engagement = {
                "views": statistics.mean([e.get("views", 0) for e in engagements]) if engagements else 0,
                "likes": statistics.mean([e.get("likes", 0) for e in engagements]) if engagements else 0,
                "shares": statistics.mean([e.get("shares", 0) for e in engagements]) if engagements else 0
            }
            
            return {
                "caption": caption,
                "uses": caption_data.get("uses", 0),
                "avg_engagement": avg_engagement,
                "total_performance_score": sum(avg_engagement.values())
            }
        
        return {"caption": caption, "uses": 0, "message": "No data available"}
    
    def export_analytics(self, filepath: Optional[str] = None) -> str:
        """
        Export all analytics data
        
        Args:
            filepath: Optional custom export path
            
        Returns:
            Path to exported file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = DATASETS_DIR / f"analytics_export_{timestamp}.json"
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "logs": self.logs,
            "engagement_data": self.engagement_data,
            "learning_signals": self.learning_signals,
            "stats": self.get_stats(days=30)
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Analytics exported to: {filepath}")
        return str(filepath)
    
    # ========== MongoDB Query Methods ==========
    
    def get_all_memes_from_db(self, limit: int = 50, skip: int = 0) -> List[Dict]:
        """
        Get all memes from MongoDB
        
        Args:
            limit: Number of results
            skip: Number of records to skip (pagination)
            
        Returns:
            List of meme documents
        """
        if not self.use_mongodb:
            logger.warning("MongoDB not available, returning from JSON logs")
            return self.logs[-limit:]
        
        try:
            cursor = self.memes_collection.find().sort("timestamp", -1).skip(skip).limit(limit)
            memes = list(cursor)
            
            # Convert ObjectId to string
            for meme in memes:
                if "_id" in meme:
                    meme["_id"] = str(meme["_id"])
                if "timestamp" in meme and isinstance(meme["timestamp"], datetime):
                    meme["timestamp"] = meme["timestamp"].isoformat()
            
            logger.info(f"✅ Retrieved {len(memes)} memes from MongoDB")
            return memes
        except Exception as e:
            logger.error(f"❌ Failed to query MongoDB: {e}")
            return []
    
    def get_meme_by_id(self, event_id: str) -> Optional[Dict]:
        """
        Get single meme by event_id from MongoDB
        
        Args:
            event_id: Event ID
            
        Returns:
            Meme document or None
        """
        if not self.use_mongodb:
            logger.warning("MongoDB not available, searching JSON logs")
            for log in self.logs:
                if log.get("event_id") == event_id:
                    return log
            return None
        
        try:
            meme = self.memes_collection.find_one({"event_id": event_id})
            
            if meme:
                if "_id" in meme:
                    meme["_id"] = str(meme["_id"])
                if "timestamp" in meme and isinstance(meme["timestamp"], datetime):
                    meme["timestamp"] = meme["timestamp"].isoformat()
                logger.info(f"✅ Found meme in MongoDB: {event_id}")
                return meme
            else:
                logger.warning(f"⚠️ Meme not found in MongoDB: {event_id}")
                return None
        except Exception as e:
            logger.error(f"❌ Failed to query MongoDB: {e}")
            return None
    
    def get_top_memes_from_db(self, limit: int = 10, metric: str = "likes") -> List[Dict]:
        """
        Get top performing memes from MongoDB
        
        Args:
            limit: Number of results
            metric: Engagement metric (likes, shares, views, downloads)
            
        Returns:
            List of top memes
        """
        if not self.use_mongodb:
            return self.get_top_performing_memes(limit, metric)
        
        try:
            cursor = self.memes_collection.find().sort(f"engagement.{metric}", -1).limit(limit)
            memes = list(cursor)
            
            # Convert ObjectId to string
            for meme in memes:
                if "_id" in meme:
                    meme["_id"] = str(meme["_id"])
                if "timestamp" in meme and isinstance(meme["timestamp"], datetime):
                    meme["timestamp"] = meme["timestamp"].isoformat()
            
            logger.info(f"✅ Retrieved top {len(memes)} memes by {metric} from MongoDB")
            return memes
        except Exception as e:
            logger.error(f"❌ Failed to query top memes: {e}")
            return []
    
    def get_memes_by_rating(self, min_rating: float = 4.0, limit: int = 20) -> List[Dict]:
        """
        Get highly rated memes from MongoDB
        
        Args:
            min_rating: Minimum rating (1-5)
            limit: Number of results
            
        Returns:
            List of highly rated memes
        """
        if not self.use_mongodb:
            logger.warning("MongoDB not available")
            return []
        
        try:
            cursor = self.memes_collection.find({
                "engagement.rating": {"$gte": min_rating}
            }).sort("engagement.rating", -1).limit(limit)
            
            memes = list(cursor)
            
            # Convert ObjectId to string
            for meme in memes:
                if "_id" in meme:
                    meme["_id"] = str(meme["_id"])
                if "timestamp" in meme and isinstance(meme["timestamp"], datetime):
                    meme["timestamp"] = meme["timestamp"].isoformat()
            
            logger.info(f"✅ Retrieved {len(memes)} memes with rating >= {min_rating}")
            return memes
        except Exception as e:
            logger.error(f"❌ Failed to query rated memes: {e}")
            return []
    
    def get_mongodb_stats(self) -> Dict:
        """
        Get statistics from MongoDB
        
        Returns:
            Stats dictionary
        """
        if not self.use_mongodb:
            logger.warning("MongoDB not available")
            return {"status": "MongoDB not connected"}
        
        try:
            total_memes = self.memes_collection.count_documents({})
            rated_memes = self.memes_collection.count_documents({"engagement.rating": {"$ne": None}})
            
            # Get average rating
            pipeline = [
                {"$match": {"engagement.rating": {"$ne": None}}},
                {"$group": {
                    "_id": None,
                    "avg_rating": {"$avg": "$engagement.rating"},
                    "total_likes": {"$sum": "$engagement.likes"},
                    "total_shares": {"$sum": "$engagement.shares"},
                    "total_downloads": {"$sum": "$engagement.downloads"}
                }}
            ]
            
            agg_result = list(self.memes_collection.aggregate(pipeline))
            
            stats = {
                "status": "✅ MongoDB connected",
                "total_memes": total_memes,
                "rated_memes": rated_memes,
                "average_rating": round(agg_result[0]["avg_rating"], 2) if agg_result else 0,
                "total_likes": agg_result[0]["total_likes"] if agg_result else 0,
                "total_shares": agg_result[0]["total_shares"] if agg_result else 0,
                "total_downloads": agg_result[0]["total_downloads"] if agg_result else 0
            }
            
            logger.info(f"✅ MongoDB stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"❌ Failed to get MongoDB stats: {e}")
            return {"status": f"Error: {e}"}


# Singleton instance
_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    """Get or create Analytics Service singleton"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service