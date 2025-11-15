from dotenv import load_dotenv
import os

# Load .env file explicitly
load_dotenv()

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    mongodb_uri: str = Field(
        default="mongodb://localhost:27017",
        description="Connection string for MongoDB.",
    )
    mongodb_db_name: str = Field(
        default="aimemeforge",
        description="Database name for the application.",
    )
    mongodb_timeout_ms: int = Field(
        default=5000,
        description="Server selection timeout for Mongo connections.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
