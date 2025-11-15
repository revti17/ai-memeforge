"""
Test if MongoDB Atlas connection works with the updated config
"""

from config import get_settings

settings = get_settings()

print("=" * 60)
print("📋 Configuration Loaded:")
print("=" * 60)
print(f"MongoDB URI: {settings.mongodb_uri[:50]}...")
print(f"Database Name: {settings.mongodb_db_name}")
print(f"Timeout (ms): {settings.mongodb_timeout_ms}")
print("=" * 60)

# Test if it's Atlas or localhost
if "mongodb+srv://" in settings.mongodb_uri:
    print("✅ Using MongoDB Atlas (Cloud)")
elif "localhost" in settings.mongodb_uri or "127.0.0.1" in settings.mongodb_uri:
    print("⚠️ Using Local MongoDB")
else:
    print("🔍 Using custom MongoDB URI")

print("\n🔄 Testing connection...")

try:
    from db.mongo_sync import connect_to_mongo_sync, get_database_sync
    
    connect_to_mongo_sync()
    db = get_database_sync()
    
    # Test connection with a ping
    result = db.command("ping")
    
    print("✅ MongoDB connection successful!")
    print(f"✅ Connected to database: {db.name}")
    
    # Check collections
    collections = db.list_collection_names()
    print(f"📊 Collections found: {len(collections)}")
    if collections:
        print(f"   Collections: {', '.join(collections)}")
    
    # Check meme_generations collection
    if "meme_generations" in collections:
        count = db["meme_generations"].count_documents({})
        print(f"🎨 Memes in database: {count}")
    
    print("\n🎉 MongoDB Atlas is configured correctly!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check your MongoDB Atlas cluster is running")
    print("2. Verify IP whitelist (0.0.0.0/0 for all IPs)")
    print("3. Confirm username/password are correct")
    print("4. Check internet connection")
