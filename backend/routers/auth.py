"""
Authentication router for Google OAuth
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt
import logging
from db.mongo_sync import get_database_sync

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# JWT Secret - In production, use environment variable
JWT_SECRET = "your-secret-key-change-this-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 30


class GoogleAuthRequest(BaseModel):
    token: str
    email: str
    name: str
    picture: Optional[str] = None


class AuthResponse(BaseModel):
    user: dict
    token: str
    message: str


@router.post("/google", response_model=AuthResponse)
async def google_auth(auth_data: GoogleAuthRequest):
    """
    Authenticate user with Google OAuth token
    Creates user if doesn't exist, updates last_login if exists
    """
    try:
        db = get_database_sync()
        users_collection = db["users"]
        
        # Extract Google ID from email or use email as ID
        google_id = auth_data.email
        
        # Check if user exists
        existing_user = users_collection.find_one({"email": auth_data.email})
        
        if existing_user:
            # Update last login
            users_collection.update_one(
                {"email": auth_data.email},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            user_data = existing_user
            logger.info(f"User logged in: {auth_data.email}")
        else:
            # Create new user
            new_user = {
                "email": auth_data.email,
                "name": auth_data.name,
                "picture": auth_data.picture,
                "google_id": google_id,
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
            }
            result = users_collection.insert_one(new_user)
            new_user["_id"] = str(result.inserted_id)
            user_data = new_user
            logger.info(f"New user created: {auth_data.email}")
        
        # Convert ObjectId to string
        if "_id" in user_data:
            user_data["_id"] = str(user_data["_id"])
        
        # Generate JWT token
        token_payload = {
            "sub": user_data.get("email"),
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return AuthResponse(
            user={
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture"),
                "id": user_data.get("_id"),
            },
            token=token,
            message="Successfully authenticated"
        )
        
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.get("/verify")
async def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"valid": True, "user": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/users")
async def get_all_users(limit: int = 100):
    """
    Get all registered users (Admin endpoint)
    Returns list of users with their login information
    """
    try:
        db = get_database_sync()
        users_collection = db["users"]
        
        # Get all users, sorted by last login (most recent first)
        users = list(users_collection.find().sort("last_login", -1).limit(limit))
        
        # Convert ObjectId to string and format dates
        formatted_users = []
        for user in users:
            formatted_users.append({
                "id": str(user["_id"]),
                "email": user.get("email"),
                "name": user.get("name"),
                "picture": user.get("picture"),
                "created_at": user.get("created_at").isoformat() if user.get("created_at") else None,
                "last_login": user.get("last_login").isoformat() if user.get("last_login") else None,
            })
        
        return {
            "total_users": len(formatted_users),
            "users": formatted_users
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")
