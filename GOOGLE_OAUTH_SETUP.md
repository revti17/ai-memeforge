# 🔐 Google OAuth Setup Guide

## ✅ What's Been Added

I've implemented **Google OAuth authentication** for your AI MemeForge application!

---

## 🎯 Features Implemented

### Frontend:
1. **Login Page** with Google Sign-In button
2. **User Dashboard** showing stats and recent memes
3. **Auth Context** for managing authentication state
4. **Protected Routes** - users must login to use the app
5. **Header Updates** with user profile pic, dashboard, and logout
6. **Beautiful UI** with animations and gradients

### Backend:
1. **Auth Router** (`/auth/google`) for Google OAuth
2. **JWT Token Generation** for secure sessions
3. **User Model** storing user data in MongoDB
4. **Users Collection** in MongoDB Atlas

---

## 🚀 Setup Instructions

### Step 1: Get Google OAuth Client ID

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create/Select Project:**
   - Click "Select a project" → "New Project"
   - Name it "AI MemeForge" → Create

3. **Enable Google OAuth:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Choose "External" → Create
   - Fill in:
     - App name: `AI MemeForge`
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue" through all steps

4. **Create OAuth Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "AI MemeForge Web Client"
   
5. **Configure Origins and Redirect URIs:**
   ```
   Authorized JavaScript origins:
   - http://localhost:5173
   - http://localhost:3000
   
   Authorized redirect URIs:
   - http://localhost:5173
   - http://localhost:3000
   ```

6. **Copy Client ID:**
   - Click "Create"
   - Copy the "Client ID" (starts with something like `123456789-abc...googleusercontent.com`)

### Step 2: Update Frontend .env

Edit `/frontend/.env`:

```bash
VITE_API_BASE=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=YOUR_ACTUAL_CLIENT_ID_HERE
```

Replace `YOUR_ACTUAL_CLIENT_ID_HERE` with the Client ID you copied.

### Step 3: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 📱 How It Works

### User Flow:

1. **User visits website** → Sees beautiful login page
2. **Clicks "Sign in with Google"** → Google OAuth popup
3. **Authorizes access** → Backend creates/updates user in MongoDB
4. **Gets JWT token** → Stored in localStorage
5. **Redirected to app** → Full access to meme generation
6. **Can view dashboard** → See their stats and recent memes
7. **Clicks logout** → Clears session, back to login

### Authentication Flow:

```
Frontend (LoginPage.jsx)
    ↓ Google OAuth
Google Sign-In
    ↓ credential
Backend (/auth/google)
    ↓ verify + create/update user
MongoDB Atlas (users collection)
    ↓ generate JWT
Frontend (AuthContext)
    ↓ store token
User Authenticated ✅
```

---

## 🗄️ MongoDB Collections

### New `users` Collection:
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://...",
  "google_id": "user@example.com",
  "created_at": "2025-11-16T...",
  "last_login": "2025-11-16T..."
}
```

---

## 🎨 New Components

### 1. LoginPage (`src/components/auth/LoginPage.jsx`)
- Beautiful animated login page
- Google Sign-In button
- Features list
- Brand messaging

### 2. UserDashboard (`src/components/dashboard/UserDashboard.jsx`)
- User stats (total memes, downloads)
- Recent creations gallery
- Profile information

### 3. AuthContext (`src/context/AuthContext.jsx`)
- Global authentication state
- Login/logout functions
- Token management
- Auto-login on refresh

---

## 🔧 Backend Endpoints

### POST `/auth/google`
Authenticate with Google OAuth token

**Request:**
```json
{
  "token": "eyJhbGc...",
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://..."
}
```

**Response:**
```json
{
  "user": {
    "email": "user@example.com",
    "name": "John Doe",
    "picture": "https://...",
    "id": "..."
  },
  "token": "jwt_token_here",
  "message": "Successfully authenticated"
}
```

### GET `/auth/verify?token=...`
Verify JWT token validity

---

## 🎯 Testing

### Test Login Flow:

1. **Start both backend and frontend**
2. **Visit:** http://localhost:5173
3. **Should see:** Login page (not the main app)
4. **Click:** "Sign in with Google"
5. **Authorize:** Allow access
6. **Should see:** Main app with your name and profile pic in header
7. **Click:** "Dashboard" to see your dashboard
8. **Click:** "Logout" to sign out

### Test MongoDB:

```bash
mongosh

# Check if user was created
use aimemeforge
db.users.find().pretty()
```

---

## 🐛 Troubleshooting

### "Google Client ID not found" error:
- Make sure you've set `VITE_GOOGLE_CLIENT_ID` in `/frontend/.env`
- Restart frontend after changing .env: `npm run dev`

### "Origin not allowed" error:
- Add `http://localhost:5173` to Authorized JavaScript origins in Google Cloud Console
- Wait 5 minutes for changes to propagate

### Backend auth errors:
- Check backend is running: `http://localhost:8000`
- Check MongoDB connection: Look for "✅ Connected to MongoDB Atlas"
- Install PyJWT: `pip install PyJWT`

### User not saved to MongoDB:
- Check MongoDB Atlas is accessible
- Check backend logs for errors
- Verify connection string in `/backend/.env`

---

## 📝 Environment Variables Summary

### Frontend `/frontend/.env`:
```bash
VITE_API_BASE=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
```

### Backend `/backend/.env`:
```bash
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=aimemeforge
HF_TOKEN=hf_...
API_KEY=sk-or-v1-...
```

---

## 🎉 What's Next

After setting up Google OAuth:

1. ✅ Users must sign in to use the app
2. ✅ Each user gets a personalized dashboard
3. ✅ User data saved to MongoDB Atlas
4. ✅ Secure JWT authentication
5. ✅ Profile pictures in header
6. ✅ Track user-specific memes (future: link memes to users)

---

## 🔒 Security Notes

- JWT tokens expire after 30 days
- Tokens stored in localStorage (consider httpOnly cookies for production)
- Change `JWT_SECRET` in `/backend/routers/auth.py` to a secure random string
- Never commit Client ID/Secrets to git
- Use environment variables for all sensitive data

---

## 📚 Files Modified/Created

**Frontend:**
- ✅ `src/App.jsx` - Added auth provider and login check
- ✅ `src/context/AuthContext.jsx` - Auth state management
- ✅ `src/components/auth/LoginPage.jsx` - Login UI
- ✅ `src/components/dashboard/UserDashboard.jsx` - User dashboard
- ✅ `src/components/layout/AppHeader.jsx` - Added logout + dashboard
- ✅ `frontend/.env` - Google Client ID config

**Backend:**
- ✅ `routers/auth.py` - Authentication endpoints
- ✅ `models/user.py` - User data model
- ✅ `main.py` - Added auth router
- ✅ `requirements.txt` - Added PyJWT

---

## 🎨 Design Preserved

✅ **Your existing design is untouched!**
- All original components work exactly the same
- Same beautiful gradients and animations
- Only added login page and dashboard
- Header updated with auth buttons

---

**Need help?** Check the troubleshooting section or review the code comments!
