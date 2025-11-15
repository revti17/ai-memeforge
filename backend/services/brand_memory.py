"""
Brand Memory Service
Handles brand logo, tone, voice, hashtags, and personalization logic.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
from colorthief import ColorThief
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"
BRAND_FILE = DATASETS_DIR / "brand_memory.json"
LOGOS_DIR = DATASETS_DIR / "logos"

LOGOS_DIR.mkdir(exist_ok=True)
DATASETS_DIR.mkdir(exist_ok=True)


class BrandMemory:
    """
    Persistent storage and analysis for brand identity.
    Stores logo, colors, tone, voice, hashtags, keywords, and caption history.
    """

    def __init__(self):
        self.brand_data = self._load_brand_data()

    # ---------------------- LOAD & SAVE ----------------------

    def _load_brand_data(self) -> Dict:
        """Load brand memory JSON file."""
        if BRAND_FILE.exists():
            try:
                with open(BRAND_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load brand memory: {e}")
        return self._get_default_brand_data()

    def _save_brand_data(self):
        """Save brand memory to disk."""
        try:
            with open(BRAND_FILE, "w") as f:
                json.dump(self.brand_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save brand memory: {e}")

    def _get_default_brand_data(self) -> Dict:
        """Default brand state."""
        return {
            "brand_name": "Default Brand",
            "tone": "humorous",
            "voice": "casual",
            "target_audience": "general",
            "logo_path": None,
            "colors": {"primary": "#FFFFFF", "secondary": "#000000"},
            "hashtags": ["#meme", "#funny", "#trending"],
            "keywords": [],
            "caption_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    # ---------------------- LOGO & COLORS ----------------------

    def save_logo(self, logo_bytes: bytes, filename: str) -> str:
        """Save brand logo file."""
        logo_path = LOGOS_DIR / filename
        with open(logo_path, "wb") as f:
            f.write(logo_bytes)
        logger.info(f"Saved brand logo: {logo_path}")

        # Extract colors and update
        try:
            colors = self.extract_colors_from_logo(logo_path)
            self.brand_data["colors"] = colors
            self.brand_data["logo_path"] = str(logo_path)
            self._save_brand_data()
        except Exception as e:
            logger.warning(f"Failed to extract colors from logo: {e}")

        return str(logo_path)

    def extract_colors_from_logo(self, logo_path: Path) -> Dict[str, str]:
        """Extract dominant colors from logo using ColorThief."""
        color_thief = ColorThief(logo_path)
        primary_rgb = color_thief.get_color(quality=1)
        secondary_rgb = color_thief.get_palette(color_count=2)[-1] if color_thief else (0, 0, 0)

        def rgb_to_hex(rgb): return "#{:02x}{:02x}{:02x}".format(*rgb)

        return {
            "primary": rgb_to_hex(primary_rgb),
            "secondary": rgb_to_hex(secondary_rgb)
        }

    # ---------------------- BRAND CONFIG ----------------------

    def update_brand(
        self,
        brand_name: Optional[str] = None,
        logo_path: Optional[str] = None,
        tone: Optional[str] = None,
        voice: Optional[str] = None,
        target_audience: Optional[str] = None,
        hashtags: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """Update brand properties."""
        if brand_name:
            self.brand_data["brand_name"] = brand_name
        if logo_path:
            self.brand_data["logo_path"] = logo_path
        if tone:
            self.brand_data["tone"] = tone
        if voice:
            self.brand_data["voice"] = voice
        if target_audience:
            self.brand_data["target_audience"] = target_audience
        if hashtags is not None:
            self.brand_data["hashtags"] = hashtags
        if keywords is not None:
            self.brand_data["keywords"] = keywords

        self.brand_data["updated_at"] = datetime.now().isoformat()
        self._save_brand_data()

        logger.info(f"Brand updated: {self.brand_data['brand_name']}")
        return self.brand_data

    # ---------------------- CONTEXT ----------------------

    def get_brand_context(self) -> Dict:
        """Get complete brand context (used by AI engine)."""
        return self.brand_data

    def export_brand_profile(self) -> Dict:
        """Export brand data."""
        return self.brand_data

    def import_brand_profile(self, profile: Dict):
        """Import brand profile."""
        self.brand_data = profile
        self.brand_data["updated_at"] = datetime.now().isoformat()
        self._save_brand_data()
        logger.info("Brand profile imported successfully.")

    def reset_brand(self):
        """Reset brand to default settings."""
        self.brand_data = self._get_default_brand_data()
        self._save_brand_data()
        logger.info("Brand reset to default configuration.")

    # ---------------------- CAPTION HISTORY ----------------------

    def add_caption_to_history(self, caption: str, engagement: Optional[Dict] = None):
        """Save generated captions to brand history."""
        self.brand_data.setdefault("caption_history", []).append({
            "caption": caption,
            "timestamp": datetime.now().isoformat(),
            "engagement": engagement or {}
        })
        self._save_brand_data()
        logger.info(f"Added caption to history: {caption}")

    def get_caption_history(self, limit: int = 20) -> List[Dict]:
        """Get recent caption history."""
        return self.brand_data.get("caption_history", [])[-limit:]

    # ---------------------- HASHTAGS ----------------------

    def get_recommended_hashtags(self, caption: str, max_tags: int = 5) -> List[str]:
        """
        Generate personalized hashtags based on caption + brand tone + history.
        """
        hashtags = set(self.brand_data.get("hashtags", []))

        if "funny" in caption.lower():
            hashtags.add("#funny")
        if "monday" in caption.lower():
            hashtags.add("#MondayMotivation")
        if self.brand_data.get("tone") == "professional":
            hashtags.add("#BusinessMeme")
        if self.brand_data.get("voice") == "casual":
            hashtags.add("#Relatable")

        # Add brand name tag
        brand_name = self.brand_data.get("brand_name", "").replace(" ", "")
        if brand_name:
            hashtags.add(f"#{brand_name}")

        return list(hashtags)[:max_tags]


# Singleton Instance
_brand_memory = None


def get_brand_memory() -> BrandMemory:
    """Get or create singleton BrandMemory instance."""
    global _brand_memory
    if _brand_memory is None:
        _brand_memory = BrandMemory()
    return _brand_memory
