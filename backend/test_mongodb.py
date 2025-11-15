"""
Test MongoDB Connection and Data Storage
Run this to verify MongoDB integration is working
"""

from db.mongo_sync import connect_to_mongo_sync, get_database_sync
from datetime import datetime


def test_connection():
    """Test MongoDB connection"""
    print("🔄 Testing MongoDB connection...")
    
    try:
        connect_to_mongo_sync()
        db = get_database_sync()
        
        # Test insert
        test_collection = db["test_collection"]
        result = test_collection.insert_one({
            "test": "data",
            "timestamp": datetime.now(),
            "message": "MongoDB is working!"
        })
        
        print(f"✅ MongoDB connected successfully!")
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Test query
        doc = test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Retrieved document: {doc}")
        
        # Clean up
        test_collection.delete_one({"_id": result.inserted_id})
        print(f"✅ Test document deleted")
        
        # Check meme_generations collection
        memes_collection = db["meme_generations"]
        count = memes_collection.count_documents({})
        print(f"\n📊 Current meme_generations collection count: {count}")
        
        if count > 0:
            print("\n🎨 Recent memes:")
            for meme in memes_collection.find().sort("timestamp", -1).limit(3):
                print(f"  - {meme.get('event_id')}: {meme.get('prompt', 'N/A')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    
    if success:
        print("\n🎉 MongoDB integration is working perfectly!")
    else:
        print("\n⚠️ MongoDB integration failed. Check your connection settings.")

