"""
User model for authentication
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    """MongoDB model for users"""
    
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    name: str
    picture: Optional[str] = None
    google_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
