# MongoDB Integration for AI MemeForge

## ✅ What's Been Added

Your backend now saves **all meme generation data to MongoDB** in addition to JSON files!

### New Features

1. **MongoDB Storage**: All memes saved to `meme_generations` collection
2. **Engagement Tracking**: Real-time updates for likes, shares, downloads, ratings
3. **Query Endpoints**: New API endpoints to retrieve meme data
4. **Fallback System**: Automatically falls back to JSON if MongoDB unavailable

---

## 📊 MongoDB Collections

### `meme_generations` Collection
Stores all generated memes with:
- `event_id`: Unique identifier
- `timestamp`: Generation time
- `prompt`: User's original prompt
- `enhanced_prompt`: AI-enhanced prompt
- `output_path`: File path to generated meme
- `filename`: Meme filename
- `caption`: Generated caption
- `trends_used`: Array of trending topics used
- `brand_settings`: Brand customization data
- `engagement`: Nested object with views, likes, shares, downloads, rating

### `caption_patterns` Collection (Future)
Learning signals for high-performing captions

### `prompt_examples` Collection (Future)
Learning signals for successful prompts

---

## 🚀 New API Endpoints

### 1. **Get All Memes**
```http
GET http://localhost:8000/generate/history?limit=50&skip=0
```
Returns paginated list of all generated memes.

**Response:**
```json
{
  "success": true,
  "count": 50,
  "memes": [...],
  "pagination": { "limit": 50, "skip": 0 }
}
```

### 2. **Get Specific Meme**
```http
GET http://localhost:8000/generate/meme/{event_id}
```
Example: `GET http://localhost:8000/generate/meme/gen_20251116_011526_32`

**Response:**
```json
{
  "success": true,
  "meme": {
    "event_id": "gen_20251116_011526_32",
    "prompt": "Rohit Sharma playing cricket",
    "caption": "Pedestrians crossing, Rohit Sharma batting 🚶‍♂️🏏",
    "engagement": { "likes": 5, "shares": 2, "downloads": 10, "rating": 4.5 }
  }
}
```

### 3. **Get Top Memes**
```http
GET http://localhost:8000/generate/top?limit=10&metric=likes
```
Get top memes sorted by: `likes`, `shares`, `views`, or `downloads`

### 4. **Get Highly Rated Memes**
```http
GET http://localhost:8000/generate/rated?min_rating=4.0&limit=20
```
Get memes with rating >= 4.0

### 5. **MongoDB Stats**
```http
GET http://localhost:8000/generate/stats/mongodb
```
Get MongoDB connection status and statistics.

**Response:**
```json
{
  "success": true,
  "stats": {
    "status": "✅ MongoDB connected",
    "total_memes": 145,
    "rated_memes": 23,
    "average_rating": 4.2,
    "total_likes": 342,
    "total_shares": 89,
    "total_downloads": 456
  }
}
```

---

## 🔍 How to Verify MongoDB Integration

### Option 1: Test Script
Run the test script to verify connection:
```bash
cd /Users/revtiramantripathi/Desktop/untitled\ folder\ 5/aimemeforge/backend
python test_mongodb.py
```

### Option 2: MongoDB Compass (GUI)
1. Download [MongoDB Compass](https://www.mongodb.com/products/compass)
2. Connect to: `mongodb://localhost:27017`
3. Open database: `aimemeforge`
4. View collection: `meme_generations`

### Option 3: mongosh (Terminal)
```bash
mongosh

# Then in mongosh:
use aimemeforge
db.meme_generations.find().pretty()
db.meme_generations.countDocuments()
```

### Option 4: VS Code MongoDB Extension
1. Install "MongoDB for VS Code" extension
2. Connect to `mongodb://localhost:27017`
3. Browse `aimemeforge` database

### Option 5: API Endpoint
Visit in browser:
```
http://localhost:8000/generate/stats/mongodb
```

---

## 📝 What Happens When You Generate a Meme

1. **User submits prompt** → API receives request
2. **Generation pipeline runs** → Image + caption created
3. **Data saved to MongoDB** → `meme_generations` collection
4. **Data saved to JSON** → Backup in `datasets/analytics_logs.json`
5. **Event ID returned** → `gen_20251116_011526_32`

### Data Structure in MongoDB:
```json
{
  "_id": ObjectId("..."),
  "event_id": "gen_20251116_011526_32",
  "timestamp": "2025-11-16T01:15:26.123Z",
  "prompt": "Rohit Sharma playing cricket",
  "enhanced_prompt": "A dynamic image of Rohit Sharma...",
  "output_path": "/path/to/meme_1763235921.png",
  "filename": "meme_1763235921.png",
  "caption": "Pedestrians crossing, Rohit Sharma batting 🚶‍♂️🏏 #TheBrand #OC",
  "trends_used": ["meirl", "oc", "me_irl", "pedestrians"],
  "brand_settings": {...},
  "engagement": {
    "views": 0,
    "likes": 0,
    "shares": 0,
    "downloads": 0,
    "rating": null
  }
}
```

---

## 🔄 Engagement Tracking

When users interact with memes:

### Downloads
```http
GET http://localhost:8000/generate/download/meme_1763235921.png
```
→ Automatically increments `engagement.downloads` in MongoDB

### Ratings
```http
POST http://localhost:8000/generate/rate/gen_20251116_011526_32
Body: { "rating": 4.5 }
```
→ Updates `engagement.rating` in MongoDB

---

## 🛠️ Technical Details

### Analytics Service Changes
- **Dual storage**: MongoDB + JSON (fallback)
- **Automatic retry**: Falls back to JSON if MongoDB fails
- **Async operations**: Non-blocking MongoDB queries
- **Error handling**: Graceful degradation

### Log Messages
- ✅ `Logged to MongoDB: gen_xxx (ID: ...)` → Success
- ⚠️ `MongoDB not available, falling back to JSON` → Using JSON
- ❌ `MongoDB insert failed: ...` → Error with details

---

## 🧪 Testing Your Setup

### Generate a Test Meme
1. Start your backend: `uvicorn main:app --reload`
2. Generate a meme via frontend or API
3. Check logs for: `✅ Logged to MongoDB`
4. Query the meme: `GET http://localhost:8000/generate/history`

### Verify Data Persistence
1. Generate a meme
2. Restart the backend
3. Query `GET http://localhost:8000/generate/history`
4. Your meme should still be there!

---

## 📈 MongoDB vs JSON

| Feature | MongoDB | JSON Files |
|---------|---------|------------|
| Speed | ⚡ Fast queries | 🐢 Slow for large datasets |
| Scalability | ✅ Millions of records | ❌ Limited by file size |
| Querying | ✅ Complex queries | ❌ Manual filtering |
| Backup | ✅ Auto replication | ✅ File-based backup |
| Used in project | Primary storage | Fallback/backup |

---

## 🎉 Summary

Your meme generation system now:
- ✅ Saves all memes to MongoDB
- ✅ Tracks engagement in real-time
- ✅ Provides query endpoints for analytics
- ✅ Falls back to JSON if MongoDB unavailable
- ✅ Maintains backward compatibility

**Next time you generate a meme, check the logs for `✅ Logged to MongoDB`!**
