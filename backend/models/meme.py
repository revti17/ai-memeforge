"""
MongoDB Models for Meme Generation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class EngagementMetrics(BaseModel):
    """Engagement tracking"""
    views: int = 0
    likes: int = 0
    shares: int = 0
    downloads: int = 0
    rating: Optional[float] = None


class MemeGeneration(BaseModel):
    """MongoDB model for meme generation events"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    event_id: str
    event_type: str = "generation"
    timestamp: datetime
    prompt: str
    enhanced_prompt: Optional[str] = None
    output_path: str
    filename: str
    caption: str
    trends_used: Optional[List[str]] = []
    brand_settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = {}
    engagement: EngagementMetrics = Field(default_factory=EngagementMetrics)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CaptionPattern(BaseModel):
    """MongoDB model for caption patterns (learning signals)"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    caption: str
    prompt: str
    rating: float
    engagement: Dict[str, Any]
    timestamp: datetime
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PromptExample(BaseModel):
    """MongoDB model for prompt examples (learning signals)"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_input: str
    enhanced_prompt: str
    rating: float
    timestamp: datetime
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
