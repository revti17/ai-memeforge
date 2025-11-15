# How to Check if MongoDB is Connected

## ✅ 5 Ways to Verify MongoDB Connection

### 1. **Run Test Script** (Recommended)
```bash
cd backend
python3 test_mongodb.py
```

**Expected Output:**
```
🔄 Testing MongoDB connection...
✅ MongoDB connected successfully!
✅ Test document inserted with ID: ...
✅ Retrieved document: {...}
✅ Test document deleted
📊 Current meme_generations collection count: 0
🎉 MongoDB integration is working perfectly!
```

---

### 2. **Check Backend Logs**
When you start your backend with `uvicorn main:app --reload`, look for:

```
INFO:db.mongo:Connected to MongoDB at mongodb://localhost:27017
INFO:services.analytics:✅ AnalyticsService initialized with MongoDB
```

If you see:
```
⚠️ MongoDB not available, falling back to JSON
```
Then MongoDB is NOT connected.

---

### 3. **Use API Endpoint**
Once your backend is running, visit:
```
http://localhost:8000/generate/stats/mongodb
```

**If connected:**
```json
{
  "success": true,
  "stats": {
    "status": "✅ MongoDB connected",
    "total_memes": 0,
    "rated_memes": 0,
    "average_rating": 0,
    "total_likes": 0,
    "total_shares": 0,
    "total_downloads": 0
  }
}
```

**If NOT connected:**
```json
{
  "success": true,
  "stats": {
    "status": "MongoDB not connected"
  }
}
```

---

### 4. **MongoDB Compass (GUI Tool)**
1. Download [MongoDB Compass](https://www.mongodb.com/products/compass)
2. Open Compass
3. Connect to: `mongodb://localhost:27017`
4. If successful, you'll see:
   - `aimemeforge` database
   - `meme_generations` collection
   - Your generated memes!

---

### 5. **mongosh (Terminal)**
```bash
# Start mongosh
mongosh

# Check if running
use aimemeforge
db.meme_generations.find().pretty()
```

---

## 🔧 Troubleshooting

### MongoDB Not Running?
```bash
# macOS (Homebrew)
brew services start mongodb-community

# Linux (systemd)
sudo systemctl start mongod

# Check if running
mongosh
```

### Connection String Wrong?
Check `backend/.env`:
```bash
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=aimemeforge
```

### Port Already in Use?
MongoDB default port is `27017`. Check if it's available:
```bash
lsof -i :27017
```

---

## 📊 After Generating Memes

### Check if Memes are Saved to MongoDB

**Option 1: API**
```bash
curl http://localhost:8000/generate/history?limit=10
```

**Option 2: mongosh**
```bash
mongosh
use aimemeforge
db.meme_generations.find().pretty()
```

**Option 3: Backend Logs**
Look for:
```
INFO:services.analytics:✅ Logged to MongoDB: gen_20251116_011526_32 (ID: ...)
```

---

## 🎯 Quick Checklist

- [ ] MongoDB service is running
- [ ] Backend started without errors
- [ ] Logs show `✅ AnalyticsService initialized with MongoDB`
- [ ] Test script passes
- [ ] `/generate/stats/mongodb` endpoint returns `✅ MongoDB connected`
- [ ] After generating a meme, logs show `✅ Logged to MongoDB`
- [ ] Can query memes via `/generate/history`

If all checkboxes are ticked, **your MongoDB integration is working perfectly!** 🎉
