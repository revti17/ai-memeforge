"""
Synchronous MongoDB wrapper for services that don't use async/await
"""

import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError
from config import get_settings

logger = logging.getLogger(__name__)

_sync_client: Optional[MongoClient] = None
_sync_database: Optional[Database] = None


def connect_to_mongo_sync() -> None:
    """
    Initialize a synchronous MongoDB client and database reference.
    Used by services that don't use async/await.
    """
    global _sync_client, _sync_database

    if _sync_client:
        return

    settings = get_settings()

    try:
        _sync_client = MongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=settings.mongodb_timeout_ms,
        )
        _sync_database = _sync_client[settings.mongodb_db_name]

        # Simple health check
        _sync_database.command("ping")
        logger.info("✅ Connected to MongoDB (sync) at %s", settings.mongodb_uri)
    except PyMongoError as exc:
        logger.error("❌ Failed to connect to MongoDB (sync): %s", exc)
        raise


def close_mongo_connection_sync() -> None:
    """Close the synchronous MongoDB client."""
    global _sync_client, _sync_database

    if _sync_client:
        _sync_client.close()
        logger.info("MongoDB sync connection closed.")

    _sync_client = None
    _sync_database = None


def get_database_sync() -> Database:
    """
    Return the synchronous MongoDB database instance.

    Raises:
        RuntimeError: if called before connection is established.
    """
    if _sync_database is None:
        # Try to connect if not connected
        try:
            connect_to_mongo_sync()
            if _sync_database is None:
                raise RuntimeError("MongoDB sync connection failed.")
        except Exception as e:
            raise RuntimeError(f"MongoDB sync connection has not been initialized: {e}")
    return _sync_database
