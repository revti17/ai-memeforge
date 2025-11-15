from typing import Any, Dict, Optional, Sequence

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from db.mongo import get_database


class BaseMongoRepository:
    """Base repository providing helper CRUD operations against MongoDB."""

    collection_name: str = ""

    def __init__(self) -> None:
        if not self.collection_name:
            raise ValueError("Repository must define a collection_name.")

        database = get_database()
        self._collection: AsyncIOMotorCollection = database[self.collection_name]

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._collection

    async def insert_one(self, document: Dict[str, Any]) -> str:
        result = await self._collection.insert_one(document)
        return str(result.inserted_id)

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        document = await self._collection.find_one(query)
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document

    async def find_many(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: Optional[int] = None,
        sort: Optional[Sequence[tuple[str, int]]] = None,
    ) -> list[Dict[str, Any]]:
        cursor = self._collection.find(query or {}, projection)
        if sort:
            cursor = cursor.sort(list(sort))
        if limit:
            cursor = cursor.limit(limit)
        items = await cursor.to_list(length=limit or 100)
        for item in items:
            if "_id" in item:
                item["_id"] = str(item["_id"])
        return items

    async def update_one(
        self,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False,
    ) -> int:
        result = await self._collection.update_one(query, update, upsert=upsert)
        return result.modified_count

    async def delete_one(self, query: Dict[str, Any]) -> int:
        result = await self._collection.delete_one(query)
        return result.deleted_count

    @staticmethod
    def to_object_id(id_value: str) -> ObjectId:
        return ObjectId(id_value)


