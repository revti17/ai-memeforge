import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from config import get_settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    """
    Initialize a shared MongoDB client and database reference.

    This should be called during FastAPI startup.
    """
    global _client, _database

    if _client:
        return

    settings = get_settings()

    try:
        _client = AsyncIOMotorClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=settings.mongodb_timeout_ms,
        )
        _database = _client[settings.mongodb_db_name]

        # simple health check to fail fast if connection is invalid
        await _database.command("ping")
        logger.info("Connected to MongoDB at %s", settings.mongodb_uri)
    except PyMongoError as exc:
        logger.error("Failed to connect to MongoDB: %s", exc)
        raise


async def close_mongo_connection() -> None:
    """Close the shared MongoDB client."""
    global _client, _database

    if _client:
        _client.close()
        logger.info("MongoDB connection closed.")

    _client = None
    _database = None


def get_database() -> AsyncIOMotorDatabase:
    """
    Return the shared MongoDB database instance.

    Raises:
        RuntimeError: if called before connection is established.
    """
    if not _database:
        raise RuntimeError("MongoDB connection has not been initialized.")
    return _database


